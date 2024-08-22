import httpx
from typing import Any, Union

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.errors import ToolInvokeError
from core.tools.tool.builtin_tool import BuiltinTool

class WebscraperTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        Invoke tools to scrape web content.
        """
        try:
            url = tool_parameters.get('url', '')
            user_agent = tool_parameters.get('user_agent', '')

            # Define request body from tool_parameters
            payload = {
                "similarity_threshold": tool_parameters.get('similarity_threshold', 0.2),
                "vector_similarity_weight": tool_parameters.get('vector_similarity_weight', 0.30000000000000004),
                "rerank_id": tool_parameters.get('rerank_id', "BAAI/bge-reranker-v2-m3"),
                "question": tool_parameters.get('question', "建设背景"),
                "top_k": tool_parameters.get('top_k', 1024),
                "doc_ids": tool_parameters.get('doc_ids', []),
                "kb_id": tool_parameters.get('kb_id', "049075cc5ace11ef8e710242ac150006"),
                "page": tool_parameters.get('page', 1),
                "size": tool_parameters.get('size', 10)
            }

            if not url:
                return self.create_text_message('Please input url')

            # Send POST request
            headers = {'User-Agent': user_agent} if user_agent else {}
            result = self.post_url(url, headers=headers, json=payload)

            if tool_parameters.get('generate_summary'):
                # Summarize and return
                return self.create_text_message(self.summary(user_id=user_id, content=result))
            else:
                # Return full response
                return self.create_text_message(result)
        except httpx.HTTPError as e:
            raise ToolInvokeError(f"HTTP error occurred: {e}")
        except Exception as e:
            raise ToolInvokeError(str(e))

    def post_url(self, url: str, headers: dict = {}, json: dict = {}) -> str:
        """
        Sends a POST request to fetch data from a URL.
        """
        try:
            with httpx.Client() as client:
                response = client.post(url, headers=headers, json=json)
                response.raise_for_status()  # Raises for HTTP errors
                return response.text
        except httpx.HTTPError as e:
            raise ToolInvokeError(f"HTTP error occurred: {e}")

    def summary(self, user_id: str, content: str) -> str:
        """
        Generates a summary of the response content.
        This method needs to be implemented according to your summarization logic.
        For now, it just returns the first 100 characters of the content.
        """
        # Placeholder for the summarization logic
        return content[:100]
