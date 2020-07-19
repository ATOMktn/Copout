class Component {
    constructor(node, state) {
        this.node = node;
        this.state = state;
    }

    get getNode() {
        return this.node;
    }

    get getState() {
        return this.state;
    }

    setState(newState) {
        this.state = newState;
    }

    setNode(newNode) {
        this.node = newNode;
    }
}

const dropdown = new Component(document.querySelector('.main.navlist'), 'closed');
const dropdownBtn = new Component(document.querySelectorAll('.dropdown-btn'), '');

const openMenu = () => {
    dropdownBtn.getNode[1].style.fill = '#0275d8';
    dropdown.getNode.animate([
        { height: '0' },
        { height: '25%' },
        { height: '50%'},
        { height: '75%' },
        { height: '100%' },
    ], 150);
    dropdown.getNode.style.height = 'auto';
    dropdown.setState('open'); 
}

const closeMenu = () => {
    dropdownBtn.getNode[1].style.fill = 'white';
    dropdown.getNode.animate([
        { height: '100%' },
        { height: '75%' },
        { height: '50%' },
        { height: '25%' },
        { height: '0%' },
    ], 150);
    dropdown.getNode.style.height = '0';
    dropdown.setState('closed');
}

window.addEventListener('click', e => {
    if (dropdown.getState === 'open') closeMenu();

    if (e.target === dropdownBtn.getNode[0] || e.target === dropdownBtn.getNode[1]) {   
        dropdown.getState === 'closed' ? openMenu() : closeMenu();
    }
});