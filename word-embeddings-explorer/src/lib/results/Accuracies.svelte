<script>
    import axios from "axios";
    import { get } from "svelte/store";
    import { flip } from "svelte/animate";
    import { sineInOut } from "svelte/easing";
    import { createEventDispatcher } from "svelte";
    import { dataset, parameters } from "../stores.js";

    export let accuracies;

    let internalUpdate = false;
    const dispatch = createEventDispatcher();

    let initialised = false;
    function update()
    {
        if (initialised === false)                                          return;
        if (internalUpdate)                                                 return;
        if (accuracies.selected === false)                                  return;
        if (get(dataset) === undefined || get(parameters) === undefined)    return;

        accuracies = {
            ...accuracies,
            dataset: get(dataset),
            parameters: get(parameters),
            status: "loading",
        };

        let url = "http://127.0.0.1:5000/evaluation";
        let config = {
            params: {
                ...get(parameters),
                dataset: accuracies.dataset.id,
                fields: "v1"
            }
        };
        axios.post(url, {}, config)
             .then(response => {
                accuracies = {
                    ...accuracies,
                    status: "show",
                    accuracy: response.data.accuracy,
                };
            })
            .catch(() => {
                accuracies = {
                    ...accuracies,
                    status: "error"
                };
            });
    }
    dataset.subscribe(update);
    parameters.subscribe(update);
    initialised = true;
    update();

    function select()
    {
        dispatch("select");

        internalUpdate = true;
        dataset.set(accuracies.dataset);
        parameters.set(accuracies.parameters);
        internalUpdate = false;
    }
</script>

<button class="w-72 flex-none rounded-md overflow-hidden divide-y-2 divide-sky-200 text-white bg-teal-800 inset-ring flex flex-col"
     class:ring-4={accuracies.selected} class:ring-red-800={accuracies.selected} on:click={select}>
    {#if accuracies.status === "show"}
        <div class="flex-none px-4 py-2 text-xl text-center overflow-hidden text-ellipsis whitespace-nowrap">
            {accuracies.dataset.id}
        </div>
        <div class="w-full flex text-xl divide-x-2 divide-sky-200">
            <div class="w-1/2 p-2 text-center">{accuracies.parameters.embedding}</div>
            <div class="w-1/2 p-2 text-center">{accuracies.parameters.similarity}</div>
        </div>
        <div class="grow w-full text-2xl flex justify-center content-center flex-wrap">
            <div class="h-fit">{accuracies.accuracy}</div>
        </div>
    {:else if accuracies.status === "loading"}
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
        <div></div>
    {:else if accuracies.status === "error"}
        <div class="h-full w-full flex justify-center items-center">
            <div class="p-2 h-fit w-fit text-2xl bg-red-800 rounded-md">
                Can't evaluate dataset
            </div>
        </div>
    {/if}
</button>