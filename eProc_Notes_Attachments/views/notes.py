"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        notes.py
    Usage:
        file consists of function dealing with the notes.
    Author:
        Shilpa Ellur

"""
from django.http import JsonResponse
from django.shortcuts import render
from eProc_Notes_Attachments.Notes_Attachments.Notes_Form import *
from eProc_Notes_Attachments.Utilities.notes_attachments_specific import notes_instance_save
from eProc_Basic.Utilities.messages.messages import *


def add_notes(req):
    """
    Adding notes to the document at header level and item level along with the note type
    :param req: Gets the request with document number, type of note and note
    :return: success message if the note is added successfully
    """
    if req.method == 'POST':
        add_note_form = NotesForm(req.POST)
        if add_note_form.is_valid():
            client = req.user.client_id
            frmst = add_note_form.save(commit=False)
            notes_instance_save(frmst, client)
            return JsonResponse({'message': MSG034})
    else:
        add_note_form = NotesForm()
    return render(req, 'Shopping_Cart/sc_second_step/sc_second_step.html', {
        'add_note_form': add_note_form,
    })
