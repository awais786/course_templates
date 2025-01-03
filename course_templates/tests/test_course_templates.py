"""
Tests for pipelines.
"""
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from ddt import data, ddt
from django.test import TestCase, override_settings


from course_templates.pipeline import GithubTemplatesPipeline
from openedx_filters.course_authoring.filters import CourseTemplateRequested


class TestPipelineStepDefinition(TestCase):
    """
    Test pipeline step definition for the hooks execution mechanism.
    """

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.templates.fetch.requested.v1": {
                "pipeline": [
                    "course_templates.pipeline.GithubTemplatesPipeline",
                ],
                "fail_silently": False,
            },
        },
    )
    def test_github_template_fetch(self):
        """
        Test successful fetching of templates from GitHub.
        """
        # Set the mock return value
        # Running the filter
        result = CourseTemplateRequested.run_filter(
            source_type="github",
            **{'source_config':"https://raw.githubusercontent.com/awais786/courses/refs/heads/main/edly_courses.json"}
        )

        expected_result = [
                {
                    "courses_name": "AI Courses",
                    "zip_url": "https://raw.githubusercontent.com/awais786/courses/main/edly/AI%20Courses/course.tar.gz",
                    "metadata": {
                        "course_id": "course-v1:edX+DemoX+T2024",
                        "title": "Introduction to Open edX",
                        "description": "Learn the fundamentals of the Open edX platform, including how to create and manage courses.",
                        "thumbnail": "https://discover.ilmx.org/wp-content/uploads/2024/01/Course-image-2.webp",
                        "active": True
                    }
                },
                {
                    "courses_name": "Digital Marketing",
                    "zip_url": "https://raw.githubusercontent.com/awais786/courses/main/edly/Digital%20Marketing/course.tar.gz",
                    "metadata": {
                        "course_id": "course-v1:edX+DemoX+T2024",
                        "title": "Introduction to Open edX",
                        "description": "Learn the fundamentals of the Open edX platform, including how to create and manage courses.",
                        "thumbnail": "https://discover.ilmx.org/wp-content/uploads/2024/08/Screenshot-2024-08-22-at-4.38.09-PM.png",
                        "active": True
                    }
                },
                {
                    "courses_name": "Python Courses",
                    "zip_url": "https://raw.githubusercontent.com/awais786/courses/main/edly/Python%20Courses/course.tar.gz",
                    "metadata": {
                        "course_id": "course-v1:edX+DemoX+T2024",
                        "title": "Introduction to Open edX",
                        "description": "Learn the fundamentals of the Open edX platform, including how to create and manage courses.",
                        "thumbnail": "https://discover.ilmx.org/wp-content/uploads/2024/04/course-card-banner.png",
                        "active": True
                    }
                }
            ]

        # Assert the expected result
        self.assertEqual(result['source_config'], expected_result)
