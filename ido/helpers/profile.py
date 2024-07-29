from django.http import HttpRequest
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from todos.models import UserSetting
from django.contrib.auth import login


class ProfileManager:
    # Cache user profile check:
    __isvalid_tags = {  # is-valid or is-invalid html tag.
        "firstname": "",
        "lastname": "",
        "email": "is-valid",
        "username": "",
        "password1": "is-valid",
        "password2": "is-valid",
        "password_details": [],
    }

    def __init__(self, request: HttpRequest):
        self.request = request
        self.first_name = request.POST.get("firstname")
        self.last_name = request.POST.get("lastname")
        self.username = request.POST["username"]
        self.email = request.POST.get("email")
        self.profile_image = request.FILES.get("image")
        self.password = request.POST.get("password1")

    @property
    def get_profile_as_dict(self):
        return {'firstname': self.first_name,
                'lastname': self.last_name,
                'username': self.username,
                'email': self.email,
                'image': self.profile_image,
                }

    @property
    def get_html_validation_dict(self):
        return self.__isvalid_tags

    def check_password(self, password1, password2):
        """
        It checks two given password and updates 'values' and 'isvalid_tag' based on the result.
        it updates html_validation dictionary and profile_data dictionary.
        """
        # Password Check:
        try:
            validate_password(password1)
            assert (password1 == password2)

        except ValidationError as messages:
            self.__isvalid_tags['password1'] = 'is-invalid'
            self.__isvalid_tags['password2'] = ''
            self.__isvalid_tags["password_details"] = messages
            return True

        except AssertionError as messages:
            self.__isvalid_tags['password1'] = ''
            self.__isvalid_tags['password2'] = 'is-invalid'
            return True

        return False

    def dose_the_user_exists(self):
        """
        returns user if exists, else None.
        if user exists, it updates validation tags to user is-invalid.
        """
        user = User.objects.filter(username=self.username).first()

        if user:
            self.__isvalid_tags["username"] = "is-invalid"
            self.__isvalid_tags["password1"] = ""
            self.__isvalid_tags["password2"] = ""
            return user

        return None

    def create_the_user(self):
        user = User.objects.create_user(
            self.username, self.email, self.password
        )
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.usersetting = UserSetting.objects.create(user=user)
        if self.profile_image:
            user.profile_image = self.profile_image

        user.save()
        return user

    def update_the_user(self, password2=None):
        """
        returns True if update was successful, else returns None.
        """

        user = User.objects.get(username=self.username)

        user.first_name = self.first_name
        user.last_name = self.last_name
        user.email = self.email

        if self.profile_image:
            user.usersetting.image_profile = self.profile_image

        if self.password or password2:
            if self.check_password(self.password, password2):
                return None

        # Save all data simultaneously:
        user.usersetting.save()
        user.set_password(self.password)
        user.save()

        # relog-in the user:
        login(self.request, user)
        return user
