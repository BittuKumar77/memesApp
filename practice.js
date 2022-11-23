let username = "Bittu";
let email = "bittu@gmail.com";
let contact = 9988338822;

// json!
let data = {
    name_value : username,
    emai_value : email,
    contact_value : contact
}

console.log("***********************SERILIZATION***********************")
console.log("Before stringify: ");
console.log(data)

console.log("After stringify");
stringify_data = JSON.stringify(data);

console.log(JSON.stringify(data));
console.log(typeof(stringify_data))

console.log("***********************DE-SERILIZATION***********************")

json_data = JSON.parse(stringify_data);
console.log(json_data);
