const messages = document.querySelector('.messages');
const searchField = document.querySelector('#searchField')
const table_output = document.querySelector('.table_output')
const app_table = document.querySelector('.app_table')
const pagination_container_upper = document.querySelector('.pagination_container_upper')
const tableBody = document.querySelector('.table-body')
table_output.style.display = 'none'

//Will remove messages throughout the app after they have been displayed for 5 seconds
setTimeout(function(){ 
    messages.style.display = "none"; 
 }, 5000);

 // will be used to search the expenses of a user to returns results for key words and dates
 searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    
    if(searchValue.trim().length > 0){
      tableBody.innerHTML = '';
      pagination_container_upper.style.display = 'none';
        fetch("/search-expenses", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
          })
            .then((res) => res.json())
            .then((data) => {
             app_table.style.display = 'none'
             table_output.style.display = 'block'
             if(data.length === 0){
                table_output.innerHTML = 'No Results Found'
             }else{
              data.forEach((item)=> {
                tableBody.innerHTML+= `
                  <td>${item.date}</td>
                  <td>$${item.amount}</td>
                  <td>${item.category}</td>
                  <td>${item.description}</td>
                `
              })
            }
        })
    }else{
      app_table.style.display = 'block'
      pagination_container_upper.style.display = 'block';
      table_output.style.display = 'none'
     }
 })