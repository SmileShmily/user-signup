#!/usr/bin/env python
#

import webapp2,cgi,re,copy

form = """
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(nameerror)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(passworderror)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(verifiederror)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(emailerror)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

welpage = """
<html>
  <head>
    <title>Unit 2 Signup</title>
  </head>

  <body>
    <h2>Welcome, %s!</h2>
  </body>
</html>
"""

nameerror = "That's not a valid username."
passworderror = "That wasn't a valid password."
verifiederror = "Your passwords didn't match."
emailerror = "That's not a valid email."

emptybook = {'username':'',
    'nameerror':'',
    'passworderror':'',
    'verifiederror':'',
    'emailerror':'',
    'email':''}


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(form % emptybook)

    def post(self):
        inputbook = copy.deepcopy(emptybook)
        username = self.request.get('username')
        email = self.request.get('email')
        password = self.request.get('password')
        verify = self.request.get('verify')
        inputbook['username'] = username
        inputbook['email'] = email

        ok = True
        if not self.valid_username(username):
            inputbook['nameerror'] = nameerror
            ok = False
        if email and not self.valid_email(email):
            inputbook['emailerror'] = emailerror
            ok = False
        if not self.valid_password(password):
            inputbook['passworderror'] = passworderror
            ok = False
        if not self.verified(password,verify):
            inputbook['verifiederror'] = verifiederror
            ok = False

        if ok:
            self.redirect('/welcome?username=' + username)
        else:
            self.response.write(form % inputbook)



    def valid_email(self,email):
        EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")
        return EMAIL_RE.match(email)

    def valid_username(self,username):
        USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    def valid_password(self,password):
        PASSWORD_RE = re.compile("^.{3,20}$")
        return PASSWORD_RE.match(password)

    def verified(self,password,verify):
        return password == verify

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write(welpage % username)
  
app = webapp2.WSGIApplication([('/', MainHandler),
                                ('/welcome',WelcomeHandler)]
                                ,debug=True)
