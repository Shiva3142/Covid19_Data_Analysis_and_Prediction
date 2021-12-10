async function get_district_list(event) {
    // console.log(event.target.value);
    let district_options_data=`<label for="diatrict_name">Please choose District</label>
    <select name="district" id="diatrict_name">`
    try {
        let response=await fetch(`http://127.0.0.1:5000/get_district_names/${event}`)
        // console.log(response);
        let result=await response.json()
        // console.log(result);
        // console.log(result.district_list);
        result.district_list.forEach(element => {
            // console.log(element[0]);
            district_options_data=district_options_data+`
            <option value="${element[0]}">${element[0]}</option>
            `
        });
        district_options_data=district_options_data+`</select>`
        district_options=document.getElementById('district_options')
        district_options.innerHTML=district_options_data
    } catch (error) {
        console.log(error);
    }
}
get_district_list('MH')


// async function getdistrict_values(event) {
//     // console.log(event);
//     // console.log(event.target);
// }




function show_district_option() {
    show_options_of_visualization()
    let district_options=document.getElementById('district_options')
    district_options.style.display='flex'
}

function hide_district_option() {
    let district_options=document.getElementById('district_options')
    district_options.style.display='none'
    
}

function state_lavel_option() {
    show_options_of_visualization()
    hide_district_option()
}


function hide_options_of_visualization() {
    let optionwindow=document.getElementById('optionwindow')
    optionwindow.style.display='none'
}
function show_options_of_visualization() {
    let optionwindow=document.getElementById('optionwindow')
    optionwindow.style.display='flex'
}