from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

openai.api_key = "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"

bootstrap = Bootstrap(app)

class EvaluationForm(FlaskForm):
    # purpose = StringField('목적', validators=[DataRequired()])
    # target = StringField('대상', validators=[DataRequired()])
    achievement_criteria = StringField('성취기준', validators=[DataRequired()])
    # high_level = StringField('상', validators=[DataRequired()])
    # mid_level = StringField('중', validators=[DataRequired()])
    # low_level = StringField('하', validators=[DataRequired()])
    evaluation_content = TextAreaField('평가내용', validators=[DataRequired()])
    submit = SubmitField('평가 제출')


@app.route('/', methods=['GET', 'POST'])
def evaluate():
    form = EvaluationForm()
    if request.method == 'POST' and form.validate_on_submit():
        prompt = f"평가를 통해 초등 5학년의 성취 수준 판단하고자 함. 성취기준: {form.achievement_criteria.data}\n평가내용: {form.evaluation_content.data}\n\n 성취 수준을 '상', '중', '하' 중 하나로 평가하고 이유에 대해 구체적으로 한 문장으로 설명하세요. 출력 예시:상, 작품 속 인물의 삶과 자신의 삶을 관련지으며 감상한 내용을 효과적으로 표현함."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        result = response.choices[0].text
        flash(f"평가 결과: {result}")
        return redirect(url_for('evaluate'))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)