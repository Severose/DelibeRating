$(document).ready(function () {
    var options = [];

    $('.dmenu a').on('click', function (event) {
        event.stopPropagation();
        event.preventDefault();
    });

    $('.chk a').on('click', function () {
        var $checkbox = $(this).find(':checkbox');

        $checkbox.attr('checked', !$checkbox.attr('checked'));
        event.stopPropagation();
        event.preventDefault();
    });

    $('.rdo a').on("click", function (event) {
        var $radio_button = $(this).find(':radio');

        if (($radio_button).attr('class') === 'rdobtn1') {
            $('input[class="rdobtn1"]').prop('checked', false);
        } else {
            $('input[class="rdobtn2"]').prop('checked', false);
        }
        $radio_button.prop("checked", true);
        event.stopPropagation();
        event.preventDefault();

    });

    $('button[id="rndmbtn"]').on("click", function (event) {
        ($('form[id="search"]')).attr('action', 'random/');
    });

    $('#search').submit(function (event) {
        var $q = ($('input[name="q"]'));
        var $loc = ($('input[name="loc"]'));
        var $rad = ($('input[name="rad"]'));
        var $sort = ($('input[name="sort"]'));
        var $price = ($('input[name="price"]'));
        var $open = ($('input[name="open"]'));

        var query = String(($('input[id="q"]').val())) ? String(($('input[id="q"]').val())) : 'food';
        var location = String(($('input[id="loc"]').val())) ? String(($('input[id="loc"]').val())) : 'Irvine, CA';
        var radius = ($('input[class="rdobtn1"]:checked').is(':checked')) ? ($('input[class="rdobtn1"]:checked').attr('data-value')) : 8050;
        var sortby = ($('input[class="rdobtn2"]:checked').is(':checked')) ? ($('input[class="rdobtn2"]:checked').attr('data-value')) : 'best_match';
        var price = [];
        var opennow = ($('input[id="opennow"]').attr('checked')) ? true : false;

        event.preventDefault();

        if ($('#price1').is(':checked')) {
            price.push('1');
        }
        if ($('#price2').is(':checked')) {
            price.push('2');
        }
        if ($('#price3').is(':checked')) {
            price.push('3');
        }
        if ($('#price4').is(':checked')) {
            price.push('4');
        }
        if (price.length === 0) {
            price = ['1', '2', '3', '4'];
        }

        $q.attr('value', String(query));
        $loc.attr('value', String(location));
        $rad.attr('value', String(radius));
        $sort.attr('value', String(sortby));
        $price.attr('value', String(price));
        $open.attr('value', String(opennow));

        ($('form[id="search"]')).off('submit').submit();
    });

    $('.grp-add').on("click", function (event) {
        var $parli = $(event.target).parent();
        var $act = $parli.find($('input[name="act"]'));
        var $grp = $parli.find($('input[name="grp"]'));
        
        $act.attr('value', $parli.find('input[name="aa"]').attr('value'));
        $grp.attr('value', $parli.find('input[name="ga"]').attr('value'));
    });

    $('#vote-add').on("click", function (event) {
        var $parform = $(event.target).parent();
        var $grp = $parform.find($('input[name="grp"]'));
        
        $grp.attr('value', $parform.find('input[name="g"]').attr('value'));
    });
        
    $('input[name="q"]').autocomplete({
        source: "api/search/",
        minLength: 2,
        delay: 250,
        open: function () {
            setTimeout(function () {
                $('.ui-autocomplete').css('z-index', 99);
            }, 0);
        },
    });

    $('input[name="usr"]').autocomplete({
        source: "api/users/",
        minLength: 2,
        delay: 250,
        open: function () {
            setTimeout(function () {
                $('.ui-autocomplete').css('z-index', 99);
            }, 0);
        },
    });

    $('.star').click(function () {
        $.ajax({
            type: "POST",
            url: "/api/star",
            data: JSON.stringify({
                'element_id': $(this).attr('id')
            }),
            dataType: "json",
            success: function (response) {
                if (response.success === true) {
                    $(response.element_id).attr('class', 'btn btn-success like');
                } else {
                    $(response.element_id).attr('class', 'btn btn-secondary like');
                }
                if (response.toggled === true) {
                    $(response.element_toggled).attr('class', 'btn btn-secondary dislike');
                }
            },
            error: function (rs, e) {
                alert(e);
            }
        });
    });

    $('.like').click(function () {
        $.ajax({
            type: "POST",
            url: "/api/like",
            data: JSON.stringify({
                'element_id': $(this).attr('id'),
                'categories': $(this).attr('value')
            }),
            dataType: "json",
            success: function (response) {
                if (response.success === true) {
                    $(response.element_id).attr('class', 'btn btn-primary like');
                } else {
                    $(response.element_id).attr('class', 'btn btn-secondary like');
                }
                if (response.toggled === true) {
                    $(response.element_toggled).attr('class', 'btn btn-secondary dislike');
                }
            },
            error: function (rs, e) {
                alert(e);
            }
        });
    });

    $('.dislike').click(function () {
        $.ajax({
            type: "POST",
            url: "/api/dislike",
            data: JSON.stringify({
                'element_id': $(this).attr('id')
            }),
            dataType: "json",
            success: function (response) {
                if (response.success === true) {
                    $(response.element_id).attr('class', 'btn btn-warning dislike');
                } else {
                    $(response.element_id).attr('class', 'btn btn-secondary dislike');
                }
                if (response.toggled === true) {
                    $(response.element_toggled).attr('class', 'btn btn-secondary like');
                }
            },
            error: function (rs, e) {
                alert(e);
            }
        });
    });

    $('.vote-opt').click(function () {
        $.ajax({
            type: "POST",
            url: "/api/addopt",
            data: JSON.stringify({
                'vote_name': $(this).attr('value'),
                'element_id': $(this).attr('id'),
            }),
            dataType: "json",
            success: function (response) {
                /* Update state (button) */
            },
            error: function (rs, e) {
                /* Error condition */
            }
        });
    });

    $('.upvote').click(function () {
        $.ajax({
            type: "POST",
            url: "/api/upvote",
            data: JSON.stringify({
                'vote_name': $(this).attr('value'),
                'element_id': $(this).attr('id')
            }),
            dataType: "json",
            success: function (response) {
                if (response.success === true) {
                    $(response.element_id).attr('class', 'btn btn-success upvote');
                } else {
                    $(response.element_id).attr('class', 'btn btn-secondary upvote');
                }
                if(response.toggled === true) {
                    $(response.element_toggled).attr('class', 'btn btn-secondary downvote');
                }

                $("canvas#vote_chart").remove();
                $("div#vote_chart_report").append('<canvas id="vote_chart"></canvas>');

                var ctx = document.getElementById('vote_chart').getContext('2d');
                var vote_chart = new Chart(ctx, {
                    type: 'horizontalBar',
                    data: {
                        labels: response.chart_labels,
                        datasets: [{
                            data: response.chart_data,
                            backgroundColor: [
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(153, 102, 255, 0.2)'
                            ],
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(153, 102, 255, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true
                                }
                            }]
                        },
                        legend: {
                            display: false
                        },
                        tooltips: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    return tooltipItem.yLabel;
                                }
                            }
                        }
                    }
                });
            },
            error: function (rs, e) {
                alert(e);
            }
        });
    });

    $('.downvote').click(function () {
        $.ajax({
            type: "POST",
            url: "/api/downvote",
            data: JSON.stringify({
                'vote_name': $(this).attr('value'),
                'element_id': $(this).attr('id')
            }),
            dataType: "json",
            success: function (response) {
                if (response.success === true) {
                    $(response.element_id).attr('class', 'btn btn-danger downvote');
                } else {
                    $(response.element_id).attr('class', 'btn btn-secondary downvote');
                }
                if (response.toggled === true) {
                    $(response.element_toggled).attr('class', 'btn btn-secondary upvote');
                }

                $("canvas#vote_chart").remove();
                $("div#vote_chart_report").append('<canvas id="vote_chart"></canvas>');

                var ctx = document.getElementById('vote_chart').getContext('2d');
                var vote_chart = new Chart(ctx, {
                    type: 'horizontalBar',
                    data: {
                        labels: response.chart_labels,
                        datasets: [{
                            data: response.chart_data,
                            backgroundColor: [
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(153, 102, 255, 0.2)'
                            ],
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(153, 102, 255, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true
                                }
                            }]
                        },
                        legend: {
                            display: false
                        },
                        tooltips: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    return tooltipItem.yLabel;
                                }
                            }
                        }
                    }
                });
            },
            error: function (rs, e) {
                alert(e);
            }
        });
    });
    
    $('#vote_chart').ready(function () {
        $.ajax({
            type: "POST",
            url: "/api/update_chart",
            data: JSON.stringify({
                'vote_name': $('#vid').attr('value')
            }),
            dataType: "json",
            success: function (response) {
                var ctx = document.getElementById('vote_chart').getContext('2d');
                var vote_chart = new Chart(ctx, {
                    type: 'horizontalBar',
                    data: {
                        labels: response.chart_labels,
                        datasets: [{
                            data: response.chart_data,
                            backgroundColor: [
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(153, 102, 255, 0.2)'
                            ],
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(153, 102, 255, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true
                                }
                            }]
                        },
                        legend: {
                            display: false
                        },
                        tooltips: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    return tooltipItem.yLabel;
                                }
                            }
                        }
                    }
                });
            }
        });
    });
});

$('#search_results').ready(function () {
    var thumbnails = document.getElementsByClassName("thumbnail");

    for (var i = 0; i < thumbnails.length; i++) {
        var color1 = '3EA6FF';
        var color2 = 'ECEEEF';
        var ratio = parseFloat(thumbnails[i].getAttribute('value'));
        var hex = function (x) {
            x = x.toString(16);
            return (x.length === 1) ? '0' + x : x;
        };

        var r = Math.ceil(parseInt(color1.substring(0, 2), 16) * ratio + parseInt(color2.substring(0, 2), 16) * (1 - ratio));
        var g = Math.ceil(parseInt(color1.substring(2, 4), 16) * ratio + parseInt(color2.substring(2, 4), 16) * (1 - ratio));
        var b = Math.ceil(parseInt(color1.substring(4, 6), 16) * ratio + parseInt(color2.substring(4, 6), 16) * (1 - ratio));

        var gradient = "#" + hex(r) + hex(g) + hex(b);
        thumbnails[i].style.backgroundColor = gradient;
    }

    // Update states of Star Buttons
    var stars = document.querySelectorAll(".star.tog");

    for (var j = 0; j < stars.length; j++) {
        stars[j].setAttribute('class', 'btn btn-success star');
    }

    // Update states of Like Buttons
    var likes = document.querySelectorAll(".like.tog");

    for (var k = 0; k < likes.length; k++) {
        likes[k].setAttribute('class', 'btn btn-primary like');
    }

    // Update states of Dislike Buttons
    var dislikes = document.querySelectorAll(".dislike.tog");

    for (var l = 0; l < dislikes.length; l++) {
        dislikes[l].setAttribute('class', 'btn btn-warning dislike');
    }
});

$('#vote_results').ready(function () {
    var thumbnails = document.getElementsByClassName("thumbnail");

    for (var i = 0; i < thumbnails.length; i++) {
        var color1 = '3EA6FF';
        var color2 = 'ECEEEF';
        var ratio = parseFloat(thumbnails[i].getAttribute('value'));
        var hex = function (x) {
            x = x.toString(16);
            return (x.length === 1) ? '0' + x : x;
        };

        var r = Math.ceil(parseInt(color1.substring(0, 2), 16) * ratio + parseInt(color2.substring(0, 2), 16) * (1 - ratio));
        var g = Math.ceil(parseInt(color1.substring(2, 4), 16) * ratio + parseInt(color2.substring(2, 4), 16) * (1 - ratio));
        var b = Math.ceil(parseInt(color1.substring(4, 6), 16) * ratio + parseInt(color2.substring(4, 6), 16) * (1 - ratio));

        var gradient = "#" + hex(r) + hex(g) + hex(b);
        thumbnails[i].style.backgroundColor = gradient;
    }

    // Update states of Like Buttons
    var upvotes = document.getElementsByClassName("upvote tog");

    for (var m = 0; m < upvotes.length; m++) {
        upvotes[m].setAttribute('class', 'btn btn-success upvote');
    }

    // Update states of Dislike Buttons
    var downvotes = document.getElementsByClassName("downvote tog");

    for (var n = 0; n < downvotes.length; n++) {
        downvotes[n].setAttribute('class', 'btn btn-danger downvote');
    }
});

$(document).on("click", '[data-toggle="lightbox"]', function (event) {
    event.preventDefault();
    $(this).ekkoLightbox();
});

$('#wordcloud').ready(function () {
    var words = eval($('#wordcloud').attr('data-value'));
    $('#wordcloud').jQCloud(words, {
        width: 300,
        height: 300
    });
});