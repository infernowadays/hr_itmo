from core.models import JobDuties
from .models import *


def create_form_educations(form, educations):
    FormEducations.objects.filter(form_id=form.id).delete()
    for education in educations:
        education['university'] = University.objects.get(pk=education['university'])
        education['specialization'] = Specialization.objects.get(pk=education['specialization'])
        education = Education.objects.create(**education)
        FormEducations.objects.create(form=form, education=education)


def create_form_jobs(form, jobs):
    FormJobs.objects.filter(form_id=form.id).delete()
    for job in jobs:
        duties = job.pop('duties')
        job = Job.objects.create(**job)
        for duty in duties:
            duty = Duty.objects.create(text=duty)
            JobDuties.objects.create(job=job, duty=duty)
        FormJobs.objects.create(form=form, job=job)


def create_form_skills(form, skills):
    FormSkills.objects.filter(form_id=form.id).delete()
    for skill_text in skills:
        skill = Skill.objects.filter(text=skill_text.get('text'))

        if not skill:
            skill_text = Skill.objects.create(id=skill_text.get('id'), text=skill_text.get('text'))
        else:
            skill_text = skill.get()

        FormSkills.objects.create(form=form, skill=skill_text)
