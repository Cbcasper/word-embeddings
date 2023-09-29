<script>
    import { createEventDispatcher } from "svelte";

    export let title;
    export let options;
    export let selectedOption = options[0];

    const dispatch = createEventDispatcher();

    function select(option)
    {
        dispatch('select', option);
        selectedOption = option;
    }
</script>

<div class="flex">
    <div class="h-full my-auto font-semibold">
        {title}
    </div>
    <div class="w-fit m-2 border-2 border-sky-800 rounded-md divide-x-2 divide-sky-800 overflow-hidden">
        {#each options as option}
            <button class:bg-slate-300={selectedOption === option}
                    class="p-1 hover:bg-slate-200"
                    on:click={() => select(option)}>
                {option}
            </button>
        {/each}
    </div>
</div>