function addFn() {
            const inputEle =
                document.getElementsByTagName('input');
            const temp = inputEle[0];
            const val = temp.value;
            temp.setAttribute('id', val);
            alert('ID Added successfully!');
        }