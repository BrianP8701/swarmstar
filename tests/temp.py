from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer

from enum import Enum

class Fruits(str, Enum):
    apple = 'apple'
    banana = 'banana'
    orange = 'orange'

class Example(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    field1: str
    field2: int
    field3: Fruits
    
    @field_validator('field3')
    def validate_field3(cls, v):
        if v == 'banana':
            return Fruits.banana
        elif v == 'apple':
            return Fruits.apple
        elif v == 'orange':
            return Fruits.orange
    
    
    
example = Example(field1='hello', field2=1, field3='banana')

dump = example.model_dump()


print(dump)

