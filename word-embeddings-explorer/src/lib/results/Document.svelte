<script>
    import axios from "axios";
    import { get } from "svelte/store";
    import { flip } from "svelte/animate";
    import { sineInOut } from "svelte/easing";
    import { createEventDispatcher } from "svelte";

    import { article, parameters, dataset } from "../stores.js";

    export let ranking;
    $: maxScore = ranking.ranking === undefined ? 0 : Math.max(...ranking.ranking.map(field => field.score));
    $: minScore = ranking.ranking === undefined ? 0 : Math.min(...ranking.ranking.map(field => field.score));

    const dispatch = createEventDispatcher();

    let internalUpdate = false;
    let placeHolders = () => [...Array(20).keys()].map(() => Math.random());
    let round = (number, digits) => Math.round(number * Math.pow(10, digits)) / Math.pow(10, digits);

    let selectedArticle;

    // Adapted from:
    // License: MIT - https://opensource.org/licenses/MIT
    // Author: Michele Locati <michele@locati.it>
    // Source: https://gist.github.com/mlocati/7210513
    function percentToColor(score)
    {
        let percent = (score - minScore) / (Math.max(maxScore - minScore, 0.075)) * 100;
        if (ranking.reverse) percent = 100 - percent;

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

    let initialised = false;
    function update()
    {
        if (initialised === false)                                          return;
        if (internalUpdate)                                                 return;
        if (ranking.selected === false)                                     return;
        if (get(article) === undefined || get(parameters) === undefined)    return;

        ranking = {
            ...ranking,
            article: get(article),
            parameters: get(parameters),
            status: "loading",
        };

        let url = `http://127.0.0.1:5000/${ranking.rankingID}-ranking`;
        let data = { article: ranking.article };
        let config = {
            params: {
                ...ranking.parameters,
                dataset: get(dataset).id
            }
        };
        axios.post(url, data, config)
             .then(response => {
                ranking = {
                    ...ranking,
                    status: "show",
                    ranking: response.data.ranking.reverse(),
                    reverse: response.data.similarity_parameters.reverse,
                };
                selectedArticle = ranking.ranking[0];
            });
    }
    article.subscribe(update);
    parameters.subscribe(update);
    initialised = true;
    update();

    function select()
    {
        dispatch("select");

        internalUpdate = true;
        article.set(ranking.article);
        parameters.set(ranking.parameters);
        internalUpdate = false;
    }
</script>

{#if ranking.status === "show"}
    <div class="w-[36rem] flex-none rounded-md overflow-hidden text-white inset-ring grid grid-cols-2"
        class:ring-4={ranking.selected} class:ring-red-800={ranking.selected}>
        <div class="h-full w-full overflow-hidden flex flex-col divide-y-2 divide-sky-200 bg-sky-800">
            <button class="flex-none px-4 py-2 text-xl text-center overflow-hidden text-ellipsis whitespace-nowrap"
                    on:click={select}>
                {ranking.article.title}
            </button>
            <div class="w-full flex text-xl divide-x-2 divide-sky-200">
                <div class="w-1/2 p-2 text-center">{ranking.parameters.embedding}</div>
                <div class="w-1/2 p-2 text-center">{ranking.parameters.similarity}</div>
            </div>
            <div class="overflow-scroll divide-y-2 divide-sky-100">
                {#each ranking.ranking as field, index (field.field.id)}
                    <button class="p-2 w-full flex justify-between" class:bg-emerald-800={field === selectedArticle}
                        animate:flip={{ duration: 1000, easing: sineInOut }} on:click={() => { selectedArticle = field; }}>
                        <div class="p-1 h-fit my-auto font-semibold overflow-hidden text-ellipsis whitespace-nowrap">
                            {index + 1}. {field.field.title}
                        </div>
                        <div class="h-fit py-1 px-2 rounded-md text-slate-900"
                            style:background-color="rgb({percentToColor(field.score)}, .85)" >
                            {round(field.score, 4)}
                        </div>
                    </button>
                {/each}
            </div>
        </div>
        <div class="p-2 h-full w-full overflow-hidden text-center flex flex-col
            bg-emerald-800 border-l-4 border-red-800 border-dashed">
            <div class="text-2xl">
                {selectedArticle.field.title}
            </div>
            <div class="p-4 overflow-scroll">
                {selectedArticle.field.content}
            </div>
        </div>
    </div>
{:else if ranking.status === "loading"}
    <div class="w-[18rem] flex-none rounded-md overflow-hidden text-white inset-ring"
        class:ring-4={ranking.selected} class:ring-red-800={ranking.selected}>
        <div class="h-full w-full overflow-hidden flex flex-col divide-y-2 divide-sky-200 bg-sky-800">
            <div class="flex-none px-4 py-2 motion-safe:animate-pulse">
                <div class="h-7 w-48 mx-auto rounded-xl bg-slate-300"></div>
            </div>
            <div class="w-full flex divide-x-2 divide-sky-200">
                <div class="grow p-2">
                    <div class="motion-safe:animate-pulse h-7 w-20 mx-auto rounded-xl bg-slate-300"></div>
                </div>
                <div class="grow p-2">
                    <div class="motion-safe:animate-pulse h-7 w-20 mx-auto rounded-xl bg-slate-300"></div>
                </div>
            </div>
            {#each placeHolders() as width}
                <div class="p-2">
                    <div class="motion-safe:animate-pulse flex justify-between content-center">
                        <div class="h-6 my-auto rounded-xl bg-slate-300" style:width="{5 + width * 7.5}rem"></div>
                        <div class="h-8 w-16 px-2 rounded-md bg-slate-300"></div>
                    </div>
                </div>
            {/each}
        </div>
    </div>
{/if}