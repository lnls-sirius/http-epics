import React, { Component } from 'react';
import {getValue} from '../lib/consts';

class PV extends Component {
    constructor(props){
        super(props)
        this.state = {
            name:'',
            value:'',
            host:'',
            severity:'',
            units:''
        }
    }

    componentDidMount() {
        setInterval(()=>{
            getValue(this.props.name, (resp) => { this.setState({...resp})})
        }, 1000);
    }
    componentWillUnmount(){
        // Todo: Remove the interval!
    }

    render() {
        return (
            <tr>
                <td>{this.props.desc}</td>
                <td>{this.state.name}</td>
                <td>{this.state.value}</td>
                <td>{this.state.units}</td>
                <td>{this.state.timestamp}</td>
                <td>{this.state.severity}</td>
                <td>{this.state.host}</td>
            </tr>
        )
    }
}
export default PV;
