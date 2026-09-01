from windows_toasts import InteractableWindowsToaster, Toast, ToastInputTextBox, ToastInputSelectionBox, ToastSelection

interactableToaster = InteractableWindowsToaster('Questionnaire')
newToast = Toast(['Please enter your details'])

# A text input field asking the user for their name
newToast.AddInput(ToastInputTextBox('name', 'Your name', 'Barack Obama'))

# # Create three selections: Male, female, other, and prefer not to say
# toastSelections = (ToastSelection('male', 'Male'), ToastSelection('female', 'Female'), ToastSelection('other', 'Other'), ToastSelection('unknown', 'Prefer not to say'))
# # Initialise the selection box with a caption 'What is your gender?'. The selections are passed in, and it defaults to 'prefer not to say.'
# selectionBoxInput = ToastInputSelectionBox('gender', 'What is your gender?', toastSelections, default_selection=toastSelections[3])
# newToast.AddInput(selectionBoxInput)
#
# # For example: {'name': 'John Smith', 'gender': 'male'}
# newToast.on_activated = lambda activatedEventArgs: print(activatedEventArgs.inputs)

interactableToaster.show_toast(newToast)

