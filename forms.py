from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, \
                    SelectField
from wtforms.validators import DataRequired


class AddTaskForm(Form):
    task_id = IntegerField()
    name = StringField('Task Name', validators=[DataRequired()])
    due_date = DateField(
        'Date Due (mm/dd/yyyy)',
        validators=[DataRequired()],
        format="%m%d%y"
        )
    priority = SelectField(
        'Priority',
        validators=[DataRequired()],
        choices=[
            (str(i), i) for i in range(1, 11)
        ]
        )
    status = IntegerField('Status')


