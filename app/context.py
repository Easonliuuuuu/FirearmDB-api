from contextvars import ContextVar
from fastapi import Request

REQUEST_CTX_KEY = "request_context"
_request_ctx_var: ContextVar[Request | None] = ContextVar(REQUEST_CTX_KEY, default=None)

'''
This is a solution I saw on https://github.com/laurentS/slowapi/issues/13
'''