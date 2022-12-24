maindata=[]

async function get_Data(object) {
    try {
        let date=1
        let month=8
        for (let index = 0; index < 10; index++) {
            if (date===32) {
                date=1
                month++
            }
            let link=``
            if (date<10) {
                linkdate=`2021-0${month}-0${date}`
            } else {
                
                linkdate=`2021-0${month}-${date}`
            }
            let response=await fetch(`https://data.covid19india.org/v4/min/data-${linkdate}.min.json`)
            let result=await response.json()
            console.log(result);
            date++
            let entity={[`${linkdate}`]:result}
            maindata.push({[`${linkdate}`]:result})
        }
    } catch (error) {
        console.log(error);
    }
    console.log(maindata);
    let extradata={...maindata}
    console.log(extradata[0])
    let jsondata=JSON.stringify(maindata)
    console.log(jsondata);
}
get_Data()