"""
Tests for authoring subdomain filters.
"""
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from ddt import data, ddt
from django.test import TestCase, override_settings

from openedx_filters.course_authoring.course_templates_pipeline import GithubTemplatesPipeline
from openedx_filters.course_authoring.filters import CourseTemplateRequested, LMSPageURLRequested
from openedx_filters.filters import PipelineStep


@ddt
class TestCourseAuthoringFilters(TestCase):
    """
    Test class to verify standard behavior of the filters located in rendering views.
    You'll find test suites for:

    - LMSPageURLRequested
    """

    def test_lms_page_url_requested(self):
        """
        Test LMSPageURLRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return lms page url requested.
        """
        url = Mock()
        org = Mock()

        url_result, org_result = LMSPageURLRequested.run_filter(url, org)

        self.assertEqual(url, url_result)
        self.assertEqual(org, org_result)


class TestPipelineStepDefinition(TestCase):
    """
    Test pipeline step definition for the hooks execution mechanism.
    """

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.templates.fetch.requested.v1": {
                "pipeline": [
                    "openedx_filters.course_authoring.course_templates_pipeline.GithubTemplatesPipeline",
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
        breakpoint()
        self.assertEqual(result['source_config'], expected_result)
