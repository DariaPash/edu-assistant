from typing import Literal, Self
import yaml
from pathlib import Path
from pydantic import BaseModel

type RoleType = Literal["history_tutor", "math_tutor"]
type TemplateType = Literal["tutor_full_answer", "tutor_quick_answer"]
type LogLevelType = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class AppConfig(BaseModel):
    log_level: LogLevelType = "INFO"


class LLMConfig(BaseModel):
    model: str
    base_url: str | None = None
    timeout: float = 60.0
    max_output_tokens: int = 200


class RoleConfig(BaseModel):
    instruction: str


class Config(BaseModel):
    app: AppConfig
    llms: dict[str, LLMConfig]
    roles: dict[RoleType, RoleConfig]
    system_templates: dict[TemplateType, str]

    @classmethod
    def from_yaml_file(cls, config_path: str | Path = "config.yml") -> Self:
        config_str = Path(config_path).read_text(encoding="utf-8")
        config_dict = yaml.safe_load(config_str)
        return cls.model_validate(config_dict)

    def render_system_instructions(self, role: RoleType, template: TemplateType) -> str:
        instruction = self.roles[role].instruction.strip()
        system_template = self.system_templates[template]
        return system_template.format(role_instruction=instruction)
        
        
