# -*- coding: utf-8 -*-
from odoo import http


# class Chatgpt(http.Controller):
#     @http.route('/chatgpt/chatgpt', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/chatgpt/chatgpt/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('chatgpt.listing', {
#             'root': '/chatgpt/chatgpt',
#             'objects': http.request.env['chatgpt.chatgpt'].search([]),
#         })

#     @http.route('/chatgpt/chatgpt/objects/<model("chatgpt.chatgpt"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('chatgpt.object', {
#             'object': obj
#         })
class AttendanceController(http.Controller):


    @http.route('/attendance/login', auth='public', website=True, methods=['GET', 'POST'])
    def attendance_login(self, **kw):
        error = None

        if kw.get('login'):
            # perform login action here
            username = kw.get('username')
            password = kw.get('password')

            # check if the username and password are valid
            if username == 'valid_username' and password == 'valid_password':
                # redirect to the attendance form after successful login
                return http.redirect_with_hash('/attendance#register_attendance_menu')
            else:
                # show error message if the username and password are invalid
                error = 'Invalid login credentials'

        return http.request.render('chatgpt.attendance_login_form', {'error': error})


