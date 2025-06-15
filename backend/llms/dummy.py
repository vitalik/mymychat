import asyncio
from contextlib import asynccontextmanager
from pydantic_ai.models.test import TestModel, TestStreamedResponse
from django.utils.lorem_ipsum import paragraphs as random_paragraphs


class DummyResponse(TestStreamedResponse):
    """A dummy response class to simulate a streaming response with a delay."""

    _delay = 0.01  # Delay in seconds between words for streaming effect

    async def _get_event_iterator(self):
        async for message in super()._get_event_iterator():
            yield message
            await asyncio.sleep(self._delay)  # Simulate delay for streaming effect


class DummyModel(TestModel):
    """Dummy model that generates random text with streaming support."""

    @asynccontextmanager
    async def request_stream(self, messages: list, model_settings=None, model_request_parameters=None):
        self.last_model_request_parameters = model_request_parameters
        model_response = self._request(messages, model_settings, model_request_parameters)
        response = DummyResponse(_model_name=self._model_name, _structured_response=model_response, _messages=messages)
        yield response


_DUMMY_CODE = """
```python
def hello(name: str) -> str:
    return f"Hello, {name}!"
```
"""


def create_dummy_model() -> DummyModel:
    """Create a dummy model with random text."""
    model = DummyModel()

    model.custom_output_text = 'As Dummy Small Language Model ' + '\n'.join(
        random_paragraphs(2) + [_DUMMY_CODE] + random_paragraphs(2) + [''] + random_paragraphs(2)
    )
    return model
