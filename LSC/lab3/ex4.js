const fetch = require("node-fetch")
const fs = require('fs');

const url = 'https://submit.plgrid.pl/api/jobs'
const headers = {
    'Content-Type' : 'application/json',
    'PROXY': 'dummy'
}

const data = {
    'host' : 'zeus.cyfronet.pl',
    'working_directory': '/people/plgjano/lsc/lab3',
    'script': "#!/bin/bash -l \nloadPovray(){ \nmodule add plgrid/apps/povray\n} \n \nloadPovray && ./script6.sh"
}

const plgridDataUrl = 'https://data.plgrid.pl/list/people/plgjano/lsc/lab3/pov001.png'

downloadFile = () => {
    fetch(plgridDataUrl, {
        headers: headers
    }).then(res => {
        const fileStream = fs.createWriteStream('./img.png');
        res.body.pipe(fileStream);
        res.body.on("error", () => console.log('Write err'));
        fileStream.on("finish", () => console.log('Download finished'));
    }).catch(err =>
        console.log(err)
    )
}

monitorJob = (job_id) => {
    fetch(`${url}/${job_id}`, {
        method: 'GET',
        headers: headers
    }).then(res => 
        res.json()
    ).then(data =>{
        console.log(data.status)
        data.status === 'FINISHED'|| data.status === 404 || data.status === 'ERROR' ? downloadFile(): setTimeout(() => monitorJob(job_id), 200);
    }).catch(err => {
        console.log(err)
    })
}

submitJob = () => {
    fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
    }).then(res => 
        res.json()
    ).then(data => {
        console.log(data)
        monitorJob(data.job_id)
    }).catch(err => {
        console.log(err)
    })
}

submitJob()
