from django import forms


class Form(forms.Form):
    def get_errors(self):
        errors = self.errors.as_data()
        new_errors = {}
        for key, message_dicts in errors.items():
            for message_dict in message_dicts:
                message = str(message_dict.message)
                new_errors[key] = message
        if new_errors:
            new_errors['result'] = False
        return new_errors


class JobForm(Form):
    bk_biz_id = forms.IntegerField(error_messages={
        'invalid': '请输入正整数',
        'min_value': '请输入正整数'
    }, required=True, min_value=1)
    bk_job_id = forms.IntegerField(error_messages={
        'invalid': '请输入正整数',
        'min_value': '请输入正整数'
    }, required=True, min_value=1)
