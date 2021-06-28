$(document).ready(function(){
    let exerciseForm = document.querySelectorAll(".exercise-form")
    let container = document.querySelector("#form-container")
    let addButton = document.querySelector("#add-form")
    let totalForms = document.querySelector("#id_concreteexercise_set-TOTAL_FORMS")

    let formNum = exerciseForm.length - 1
    let emptyForm = exerciseForm[formNum].cloneNode(true)
    let formRegex = RegExp('concreteexercise_set-' + formNum + '-','g')
    addButton.addEventListener('click', addForm)

    function addForm(e) {
        e.preventDefault()

        formNum = document.querySelectorAll(".exercise-form").length
        let newForm = emptyForm.cloneNode(true)

        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `concreteexercise_set-${formNum}-`)
        container.insertBefore(newForm, addButton)

        totalForms.setAttribute('value', `${formNum+1}`)
    }
});