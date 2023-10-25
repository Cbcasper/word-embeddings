<script>
    import { createEventDispatcher, onMount } from "svelte";

    export let options;
    export let selectedOption = options[0];

    const dispatch = createEventDispatcher();

    function select(option)
    {
        dispatch('select', option);
        selectedOption = option;
    }
    onMount(() => select(options[0]));
</script>

<ul class="text-right divide-y divide-sky-800 overflow-scroll snap-y">
    {#each options as option}
        <li class:bg-slate-300={selectedOption === option} class="p-2 snap-center hover:bg-slate-200">
            <button on:click={() => select(option)}>
                {option}
            </button>
        </li>
    {/each}
</ul>