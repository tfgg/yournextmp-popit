import json
from os.path import dirname, join
from urlparse import urlsplit

from django_webtest import WebTest

from mock import patch, MagicMock

class TestConstituencyPostcodeFinderView(WebTest):

    def test_front_page(self):
        response = self.app.get('/')
        # Check that there is a form on that page
        form_postcode = response.forms['form-postcode']
        form_name = response.forms['form-name']

    def test_valid_postcode_redirects_to_constituency(self):
        response = self.app.get('/')
        form = response.forms['form-postcode']
        form['postcode'] = 'SW1A 1AA'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        split_location = urlsplit(response.location)
        self.assertEqual(
            split_location.path,
            '/constituency/65759/cities-of-london-and-westminster'
        )

    def test_unknown_postcode_returns_to_finder_with_error(self):
        response = self.app.get('/')
        form = response.forms['form-postcode']
        # This looks like a postcode to the usual postcode-checking
        # regular expressions, but doesn't actually exist
        form['postcode'] = 'CB2 8RQ'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        split_location = urlsplit(response.location)
        self.assertEqual(split_location.path, '/')
        self.assertEqual(split_location.query, 'bad_postcode=CB2%208RQ')


    def test_nonsense_postcode_returns_to_finder_with_error(self):
        response = self.app.get('/')
        form = response.forms['form-postcode']
        # This looks like a postcode to the usual postcode-checking
        # regular expressions, but doesn't actually exist
        form['postcode'] = 'foo bar'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        split_location = urlsplit(response.location)
        self.assertEqual(split_location.path, '/')
        self.assertEqual(split_location.query, 'bad_postcode=foo%20bar')


class FakeCollection(object):

    example_popit_data_directory = join(
        dirname(__file__), 'example-popit-data'
    )

    def __init__(self, *args):
        self.object_id = args[0] if len(args) == 1 else None

    def get(self, **kwargs):
        with open(join(
                self.example_popit_data_directory,
                '{0}_{1}_embed={2}.json'.format(
                    self.collection,
                    self.object_id,
                    kwargs.get('embed', 'membership')
                )
        )) as f:
                return json.load(f)


class FakePersonCollection(FakeCollection):
    collection = 'persons'


class FakeOrganizationCollection(FakeCollection):
    collection = 'organizations'


class TestConstituencyDetailView(WebTest):

    @patch('candidates.views.PopIt')
    def test_any_constituency_page(self, MockPopIt):
        MockPopIt.return_value.organizations = FakeOrganizationCollection
        MockPopIt.return_value.persons = FakePersonCollection
        # Just a smoke test for the moment:
        response = self.app.get('/constituency/65808/dulwich-and-west-norwood')
        response.mustcontain('Tessa Jowell (Labour Party)')
