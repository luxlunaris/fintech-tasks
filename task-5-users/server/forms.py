from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Regexp,
    ValidationError,
)

from .models import clients


class PhotoForm(FlaskForm):

    photo = FileField(
        "Photo",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "jpeg", "png"], "You can upload only .jpg, .jpeg and .png"
            ),
        ],
    )
    change = SubmitField("Change")


class ClientForm(FlaskForm):
    def validate_phone_num(form, field):
        for id in clients:
            if field.data == clients[id].phone_num:
                raise ValidationError(
                    "You cannot use this phone number as it is already in client base"
                )

    def validate_e_mail(form, field):
        for id in clients:
            if field.data == clients[id].e_mail:
                raise ValidationError(
                    "You cannot use this e-mail address as it is already in client base"
                )

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=40, message="Length must be between 2 and 40"),
            Regexp(
                r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",
                message="Input should contain only latin characters, whitespaces and ' or -",
            ),
        ],
    )
    phone_num = StringField(
        "Phone number",
        validators=[
            DataRequired(),
            Regexp(
                r"^[+]{0,1}[0-9][(][0-9]{1,4}[)][0-9]{3}([-][0-9]{2}){2}$",
                message="Input should be like 0(000)000-00-00 or +0(000)000-00-00",
            ),
        ],
    )
    e_mail = StringField(
        "E-mail",
        validators=[
            DataRequired(),
            Length(min=6, max=40, message="Length must be between 6 and 40"),
            Email(message="Input should be like name@domain.domain"),
        ],
    )
    add = SubmitField("Add client")
