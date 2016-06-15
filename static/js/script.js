$(document).ready(function() {

    exercise_template = _.template($("#exercise_template").html());
    

    set_template = _.template($("#set_template").html());
    

    $("#addExercise").on('click', function() {
        exercise_num = Number($("[name=exercise_count]").val()) + 1;
        $("[name=exercise_count]").val(exercise_num);

        exercise_compiled = exercise_template({exercise_num : exercise_num});
        set_compiled = set_template({exercise_num : exercise_num});

        $("#addExercise").before(exercise_compiled);
        $("#exercise" + exercise_num).append(set_compiled);
    });

    $(document).on('click', '.addSet', function() {

        exercise_num = Number($(this).attr("exercise"));

        set_compiled = set_template({exercise_num : exercise_num});
        console.log(set_compiled);
        $("#exercise" + exercise_num).append(set_compiled);
    });
});