import React, { Component } from 'react';
import { PVS } from './lib/consts';
import PV from './components/PV.jsx';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            PVS: PVS
        };
    }

    onAddItem = (value) => {
        this.setState(state => {
            const list = state.PVS.concat(value);
            return {
                PVS:list
            };
        });
    };

    renderPVs = () => {
        PVS.forEach(element => {
            console.log(element);
        });
    }

    render() {
        const items = this.state.PVS.map((d) => {
            console.log(d);
            return <PV name={d.name} desc={d.desc} key={d.name}/>
        });

        return (<div>
            {items}
        </div>);
    }
}
export default App;
