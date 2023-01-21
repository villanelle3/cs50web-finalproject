console.log('adios')

document.addEventListener('DOMContentLoaded', function ()
{
    var c = document.querySelectorAll(".likou");
    var c2 = document.querySelectorAll(".dislike");


    c.forEach(function(cm){
        cm.addEventListener('click', function(e) {
            e.preventDefault();
            let botaolike = document.getElementById(`like-${this.value}`)
            let botaodislike = document.getElementById(`dislike-${this.value}`)
            botaodislike.classList.remove("likedseta");
            botaolike.classList.add("likedseta");
            let total = document.getElementById(`total-${this.value}`)
            numero =  parseInt(total.innerHTML)
            total.innerHTML = numero + 1
            $.ajax({
                type: 'POST',
                url: `/addlike`,
                data: {
                    postid: this.value,
                    action: 'post'
                },

                success: function(data){
                    console.log('oka')
                }
            });
            });
        });

    c2.forEach(function(cm){
        cm.addEventListener('click', function(e) {
            e.preventDefault();
            let botaodislike = document.getElementById(`dislike-${this.value}`)
            let botaolike = document.getElementById(`like-${this.value}`)
            botaolike.classList.remove("likedseta");
            botaodislike.classList.add("likedseta");
            let total = document.getElementById(`total-${this.value}`)
            numero =  parseInt(total.innerHTML)
            total.innerHTML = numero - 1
            $.ajax({
                type: 'POST',
                url: `/addlike`,
                data: {
                    postid: this.value,
                    action: 'post'
                },

                success: function(data){
                    console.log('oka')
                }
            });
            });
        });
});



