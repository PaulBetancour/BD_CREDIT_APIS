from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class CreditInputSchema(BaseModel):
    id_credit: int = Field(..., gt=0, description="ID único del crédito")
    customer_id: int = Field(..., example=1082423)
    loandate: datetime
    age: float = Field(..., gt=17, lt=95, description="Edad entre 18 y 95 años")
    income: float = Field(..., ge=0)
    cupo_solicitado: float = Field(..., gt=0)
    
    @field_validator('income')
    @classmethod
    def validar_ingreso_minimo(cls, v):
        if v < 100:
            raise ValueError('Ingreso insuficiente para perfil de microcrédito')
        return v

class CreditOutputSchema(BaseModel):
    customer_id: int
    cupo_solicitado: float
    cupo_aprobado: float
    ratio_aprobacion: float
    resultado_cobranza: str