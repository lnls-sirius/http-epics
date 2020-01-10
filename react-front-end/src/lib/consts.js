import axios from 'axios'
export const WEBDIS_URL = "http://10.0.38.42/webdis";
export const GET = WEBDIS_URL + '/GET';

export const PVS = [
    // 'RA-RF:PowerSensor1:PwrAvg-Mon',
    // 'RA-RF:PowerSensor1:TracDataAvg-Mon',
    {'name':'BO-Fam:PS-B-2:Current-Mon', 'desc':'Corrente PS B2'},
    {'name':'BO-Fam:PS-B-1:Current-Mon', 'desc':'Corrente PS B1'},
    {'name':'SI-Fam:PS-B1B2-1:Current-Mon', 'desc':'Corrente PS B1B2 02'},
    {'name':'SI-Fam:PS-B1B2-2:Current-Mon', 'desc':'Corrente PS B1B2 02'},
    {'name':'BO-35D:DI-DCCT:Current-Mon', 'desc':'Corrente DCCT Booster'},
    {'name':'SI-13C4:DI-DCCT:Current-Mon', 'desc':'Corrente DCCT Anel 13C4'},
    {'name':'SI-14C4:DI-DCCT:Current-Mon', 'desc':'Corrente DCCT Anel 14C4'}];

export function getValue(pv, callback){
    const url = GET +'/'+ encodeURI(pv);
    axios.get(url)
    .then(function (response) {
        // handle success
        let data = JSON.parse(response.data.GET);
        data['name'] = pv;
        callback(data);
    })
    .catch(function (error) {
        // handle error
        console.log(error);
    })
    .finally(function () {
        // always executed
    });
}
