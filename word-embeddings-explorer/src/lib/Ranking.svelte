<script>
    import axios from "axios";
    import { flip } from "svelte/animate";
    import { sineInOut } from 'svelte/easing';

    let ranking;
    let reverse;
    $: maxScore = ranking === undefined ? 0 : Math.max(...ranking.map(field => field.score));
    $: minScore = ranking === undefined ? 0 : Math.min(...ranking.map(field => field.score));

    export function update(article, parameters)
    {
        if (article === undefined) return;
        let config = {
            params: {
                id: article.id,
                ...parameters,
            }
        };
        axios.get("http://127.0.0.1:5000/ranking", config)
             .then(response => {
                ranking = response.data.ranking;
                reverse = response.data.similarity_parameters.reverse;
                console.log(reverse);
             });
    }

    // License: MIT - https://opensource.org/licenses/MIT
    // Author: Michele Locati <michele@locati.it>
    // Source: https://gist.github.com/mlocati/7210513
    function percentToColor(score)
    {
        let percent = (score - minScore) * 100 / (maxScore - minScore);
        if (reverse) percent = 100 - percent;

        let red, green, blue = 0;
        if (percent < 50)
        {
            red = 255;
            green = Math.round(5.1 * percent);
        }
        else
        {
            green = 255;
            red = Math.round(510 - 5.10 * percent);
        }
        return [red, green, blue].join(", ");
    }

    let round = (number, digits) => Math.round(number * Math.pow(10, digits)) / Math.pow(10, digits);
</script>

<div class="flex-auto grid grid-cols-2 overflow-scroll">
    {#if ranking !== undefined}
        {#each ranking as field, index (field.field)}
            <div class="p-2 flex justify-between border border-sky-100"
                 animate:flip={{ duration: 1000, easing: sineInOut }}>
                <div class="p-1 h-fit my-auto font-semibold">
                    {index + 1}. {field.field}
                </div>
                <div class="h-fit py-1 px-2 rounded-md" style="background-color: rgb({percentToColor(field.score)}, .85)">
                    {round(field.score, 4)}
                </div>
            </div>
        {/each}
    {/if}
</div>