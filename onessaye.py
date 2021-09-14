from unittest import TestCase
import unittest.mock


class AuthenticatedObjectViewTest(unittest.TestCase):
    """ This collects the tests around the functionality provided in
        amodule.views.authenticated_object_view
    """
    def test_authenticated_object_view_arg1_is_not_none(self):
        """ Here we test the case that arg1 is not None but arg2 is none
        """
        mock_render_to_response = unittest.mock.MagicMock()
        with unittest.mock.patch.multiple(
                'amodule.views',
                render_to_response=mock_render_to_response,
                RequestContext=unittest.mock.MagicMock(),
                login_required=lambda x: x
        ):
            from amodule.views import authenticated_object_view
            mock_request = unittest.mock.Mock()
            authenticated_object_view(mock_request, 'test1', None)
            _, args, _ = mock_render_to_response.mock_calls[0]
            self.assertEquals(
                args[0],
                'a_template.html',
                'The wrong template is in our render'
            )
            self.assertEquals(
                args[1]['templ_var1'],
                1,
                'Passing the wrong template variable in'
            )
            self.assertEquals(
                args[1]['templ_var2'],
                2,
                'Passing the wrong template variable in'
            )