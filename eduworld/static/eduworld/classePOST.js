console.log("hello world!")

document.addEventListener('DOMContentLoaded', function ()
{
  document.querySelector('#newcomment').addEventListener('click', () => getdata());
});


const getdata = () =>{
    $.ajax({
        type: 'POST',
        url: '/addcomment',
        success: function(response){
            const data = response.new_comment
            const nome = response.nome
            const foto = response.foto

            console.log(data)
            console.log(nome)
            console.log(foto)

        },
        error: function(error){
            console.log(error)
        }
    })
}



