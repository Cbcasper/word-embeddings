<script>
    import axios from "axios";
    import { get } from "svelte/store";
    import { flip } from "svelte/animate";
    import { sineInOut } from 'svelte/easing';

    export let article;
    export let parameters;

    let ranking;
    let loadStatus = "none";
    let placeHolders = [...Array(20).keys()].map(() => Math.random());

    let reverse;
    $: maxScore = ranking === undefined ? 0 : Math.max(...ranking.map(field => field.score));
    $: minScore = ranking === undefined ? 0 : Math.min(...ranking.map(field => field.score));

    function update()
    {
        if (get(article) === undefined || get(parameters) === undefined) return;
        loadStatus = "loading";

        let url = "http://127.0.0.1:5000/ranking";
        let data = { article: get(article).content };
        let config = {
            params: {
                ...get(parameters),
            }
        };
        axios.post(url, data, config)
             .then(response => {
                ranking = response.data.ranking.reverse();
                reverse = response.data.similarity_parameters.reverse;
                loadStatus = "ranking";
             });
    }
    article.subscribe(update);
    parameters.subscribe(update);

    // License: MIT - https://opensource.org/licenses/MIT
    // Author: Michele Locati <michele@locati.it>
    // Source: https://gist.github.com/mlocati/7210513
    function percentToColor(score)
    {
        let percent = (score - minScore) / (Math.max(maxScore - minScore, 0.075)) * 100;
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

<div class="h-full divide-x-2 divide-sky-800 flex">
    {#if loadStatus === "ranking"}
        <div class="w-96 overflow-scroll">
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
        </div>
    {:else if loadStatus === "loading"}
        <div class="w-96 overflow-hidden">
            {#each placeHolders as width}
                <div class="p-2 border border-sky-100">
                    <div class="motion-safe:animate-pulse flex justify-between content-center">
                        <div class="h-6 my-auto rounded-xl bg-slate-300" style="width: {5 + width * 10}rem"></div>
                        <div class="h-8 w-16 px-2 rounded-md bg-slate-300"></div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if loadStatus === "none"}
        <div class="w-96"></div>
    {/if}
    <div>
    </div>
</div>