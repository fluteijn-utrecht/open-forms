from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Type, TypedDict

from json_logic import jsonLogic

from openforms.formio.service import FormioConfigurationWrapper
from openforms.forms.constants import LogicActionTypes
from openforms.forms.models import FormLogic, FormVariable
from openforms.typing import DataMapping, JSONObject
from openforms.utils.json_logic import ComponentMeta, introspect_json_logic
from openforms.variables.models import ServiceFetchConfiguration

from ..logic.binding import bind
from ..models import SubmissionStep
from ..models.submission_step import DirtyData
from .log_utils import log_errors


class ActionDetails(TypedDict):
    type: str
    property: dict
    state: Any
    value: Any


class ActionDict(TypedDict):
    component: str
    variable: str
    form_step: str
    form_step_uuid: str
    action: ActionDetails


def compile_action_operation(action: ActionDict) -> "ActionOperation":
    return ActionOperation.from_action(action)


class ActionOperation:
    rule: FormLogic

    @staticmethod
    def from_action(action: ActionDict) -> "ActionOperation":
        action_type = action["action"]["type"]
        cls = ACTION_TYPE_MAPPING[action_type]
        return cls.from_action(action)

    def apply(
        self, step: SubmissionStep, configuration: FormioConfigurationWrapper
    ) -> None:
        """
        Implements the side effects of the action operation.
        """
        pass

    def eval(self, context: DataMapping) -> DataMapping | None:
        """
        Return a mapping [name/path -> new_value] with changes that are to be
        applied to the context.
        """
        pass

    def get_action_log_data(
        self,
        component_map: Dict[str, ComponentMeta],
        all_variables: Dict[str, FormVariable],
        initial_data: dict,
    ) -> Optional[JSONObject]:
        """Get action information to log"""
        return None


@dataclass
class PropertyAction(ActionOperation):
    component: str
    property: str
    value: Any

    @classmethod
    def from_action(cls, action: ActionDict) -> "PropertyAction":
        return cls(
            component=action["component"],
            property=action["action"]["property"]["value"],
            value=action["action"]["state"],
        )

    def apply(
        self, step: SubmissionStep, configuration: FormioConfigurationWrapper
    ) -> None:
        if self.component not in configuration:
            return None
        component = configuration[self.component]
        component[self.property] = self.value

    def get_action_log_data(
        self,
        component_map: Dict[str, ComponentMeta],
        all_variables: Dict[str, FormVariable],
        initial_data: dict,
    ) -> JSONObject:

        component_meta = component_map.get(self.component)

        # figure out the best possible label
        # 1. fall back to component label if there is a label, else empty string
        # 2. if there is a variable, use the name if it's set, else fall back to
        # component label
        label = component_meta.component.get("label", "") if component_meta else ""
        if self.component in all_variables:
            label = all_variables[self.component].name or label

        return {
            "key": self.component,
            "type_display": LogicActionTypes.get_label(LogicActionTypes.property),
            "value": self.property,
            "state": self.value,
            "label": label,
        }


class DisableNextAction(ActionOperation):
    @classmethod
    def from_action(cls, action: ActionDict) -> "DisableNextAction":
        return cls()

    def apply(
        self, step: SubmissionStep, configuration: FormioConfigurationWrapper
    ) -> None:
        step._can_submit = False

    def get_action_log_data(
        self,
        component_map: Dict[str, ComponentMeta],
        all_variables: Dict[str, FormVariable],
        initial_data: dict,
    ) -> JSONObject:

        return {
            "type_display": LogicActionTypes.get_label(LogicActionTypes.disable_next),
        }


@dataclass
class StepNotApplicableAction(ActionOperation):
    form_step_identifier: str

    @classmethod
    def from_action(cls, action: ActionDict) -> "StepNotApplicableAction":
        return cls(
            form_step_identifier=action["form_step_uuid"],
        )

    def apply(
        self, step: SubmissionStep, configuration: FormioConfigurationWrapper
    ) -> None:
        execution_state = (
            step.submission.load_execution_state()
        )  # typically cached already
        submission_step_to_modify = execution_state.resolve_step(
            self.form_step_identifier
        )
        submission_step_to_modify._is_applicable = False

        # This clears data in the database to make sure that saved steps which later become
        # not-applicable don't have old data
        submission_step_to_modify.data = {}
        if submission_step_to_modify == step:
            step._is_applicable = False
            step.data = DirtyData({})

    def get_action_log_data(
        self,
        component_map: Dict[str, ComponentMeta],
        all_variables: Dict[str, FormVariable],
        initial_data: dict,
    ) -> JSONObject:
        return {
            "type_display": LogicActionTypes.get_label(
                LogicActionTypes.step_not_applicable
            ),
            "step_name": self.form_step_identifier,
        }


@dataclass
class VariableAction(ActionOperation):
    variable: str
    value: JSONObject

    @classmethod
    def from_action(cls, action: ActionDict) -> "VariableAction":
        return cls(variable=action["variable"], value=action["action"]["value"])

    def eval(self, context: DataMapping) -> DataMapping:
        with log_errors(self.value, self.rule):
            return {self.variable: jsonLogic(self.value, context)}

    def get_action_log_data(
        self,
        component_map: Dict[str, ComponentMeta],
        all_variables: Dict[str, FormVariable],
        initial_data: dict,
    ) -> JSONObject:
        # Check if it's a primitive value, which doesn't require introspection
        if not isinstance(self.value, (dict, list)):
            value = self.value
        else:
            action_logic_introspection = introspect_json_logic(
                self.value, component_map, initial_data
            )
            value = action_logic_introspection.as_string()

        return {
            "key": self.variable,
            "type_display": LogicActionTypes.get_label(LogicActionTypes.variable),
            "value": value,
        }


@dataclass
class ServiceFetchAction(ActionOperation):
    variable: str
    fetch_config: int

    @classmethod
    def from_action(cls, action: ActionDict) -> "ServiceFetchAction":
        return cls(variable=action["variable"], fetch_config=action["action"]["value"])

    def eval(self, context: DataMapping) -> DataMapping:
        # XXX bind is expressed in terms of FormVariables
        # this disguise as an Action should be temporary
        dummy_var = FormVariable(
            name=self.variable,
            service_fetch_configuration=ServiceFetchConfiguration.objects.get(
                pk=self.fetch_config
            ),
        )
        with log_errors({}, self.rule):  # TODO proper logging/error handling
            return {dummy_var.name: bind(dummy_var, context)}


ACTION_TYPE_MAPPING: Mapping[str, Type[ActionOperation]] = {
    LogicActionTypes.property: PropertyAction,
    LogicActionTypes.disable_next: DisableNextAction,
    LogicActionTypes.step_not_applicable: StepNotApplicableAction,
    LogicActionTypes.variable: VariableAction,
    LogicActionTypes.fetch_from_service: ServiceFetchAction,
}
