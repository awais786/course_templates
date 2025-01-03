"""
Pipeline steps for course templates. These will be move to some where else.
"""

import requests
from django.http import JsonResponse
from openedx_filters.filters import PipelineStep


class GithubTemplatesPipeline(PipelineStep):
    """
    A single-step pipeline to fetch templates from various sources such as GitHub or S3.
    """
    @classmethod
    def run_filter(cls, source_type, **kwargs):
        """
        Fetch templates from a specified source.
        Arguments:
            source_type (str): The type of source ('github' or 's3').
            source_config (dict): Configuration for the source (e.g., URL for GitHub, bucket/key for S3).

        Returns:
            dict: Templates fetched from the source.

        Raises:
            TemplateFetchException: If fetching templates fails.
        """
        if source_type == "github":
            return {"source_config": cls.fetch_from_github(**kwargs)}
        else:
            return {}

    @classmethod
    def fetch_from_github(cls, **kwargs):
        """
        Fetches and processes raw file data directly from raw GitHub URL.
        """
        try:
            source_url = kwargs.get('source_config')
            headers = kwargs.get('headers', {})
            if not source_url:
                return {"error": "Source URL not provided", "status": 400}

            response = requests.get(source_url, headers=headers)
            return response.json()

        except Exception as err:
            return {"error": f"Error fetching raw data: {err}", "status": 500}
