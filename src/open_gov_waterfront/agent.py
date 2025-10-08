"""
OpenAI Agents SDK integration for AI-powered engineering assistance.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


class WaterfrontAgent:
    """AI agent for waterfront engineering calculations and guidance."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini") -> None:
        """Initialize the waterfront engineering agent."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable."
            )
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        self.system_prompt = """You are an expert marine and waterfront structural engineer specializing in California, Indiana, and Ohio coastal and waterway projects.

Your expertise includes:
- Linear wave theory and coastal processes
- Pile design (Morison forces, axial capacity, scour, corrosion)
- Berthing energy and fender selection
- Mooring analysis (wind and current loads)
- Seawall stability
- Regulatory frameworks: USACE, NOAA, CA Coastal Commission, ASCE MOP 130/61, PIANC

Provide clear, engineering-focused guidance. Always remind users that these are screening-level calculations requiring professional validation and AHJ approval."""

    def query(self, user_message: str, context: dict[str, Any] | None = None) -> str:
        """Query the agent with a user message and optional context."""
        messages: list[dict[str, str]] = [{"role": "system", "content": self.system_prompt}]

        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            messages.append(
                {
                    "role": "user",
                    "content": f"Context:\n{context_str}\n\nQuestion: {user_message}",
                }
            )
        else:
            messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.7, max_tokens=1500
        )

        return response.choices[0].message.content or ""

    def suggest_calculation(self, project_description: str) -> dict[str, Any]:
        """Suggest appropriate calculations based on project description."""
        prompt = f"""Based on this waterfront project description:

{project_description}

Suggest the most relevant engineering calculations to perform and provide recommended input parameter ranges. Format your response as specific calculation recommendations."""

        response = self.query(prompt)
        return {"suggestion": response}

    def interpret_results(
        self, calculation_type: str, inputs: dict[str, Any], results: dict[str, Any]
    ) -> str:
        """Interpret calculation results and provide engineering guidance."""
        prompt = f"""Interpret these {calculation_type} calculation results:

Inputs: {inputs}
Results: {results}

Provide engineering interpretation, typical acceptance criteria, and recommendations for next steps."""

        return self.query(prompt)
