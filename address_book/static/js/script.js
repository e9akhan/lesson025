var divemailblock = document.getElementById('extendableEmail')

function addEmail(){
    var newElement = document.createElement('input')
    newElement.setAttribute('type', 'email')
    newElement.setAttribute('class', 'form-control m-1')
    newElement.setAttribute('placeholder', 'Enter Email')
    newElement.setAttribute('name', 'email')

    divemailblock.appendChild(newElement)
}

var divphoneblock = document.getElementById('extendablePhone')

function addPhone(){
    var newElement = document.createElement('input')
    newElement.setAttribute('type', 'text')
    newElement.setAttribute('class', 'form-control m-1')
    newElement.setAttribute('placeholder', 'Enter Phone No.')
    newElement.setAttribute('name', 'phone')

    divphoneblock.appendChild(newElement)
}

var divaddressblock = document.getElementById('extendableAddress')

function addAddress(){
    var newElement = document.createElement('input')
    newElement.setAttribute('type', 'text')
    newElement.setAttribute('class', 'form-control m-1')
    newElement.setAttribute('placeholder', 'Enter Address.')
    newElement.setAttribute('name', 'address')

    divaddressblock.appendChild(newElement)
}