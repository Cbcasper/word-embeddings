<script>
    import { createEventDispatcher, onMount } from "svelte";

    export let options;
    export let parameter;

    const dispatch = createEventDispatcher();

    function select(option)
    {
        parameter.set(option);
        dispatch("select");
    }
    onMount(() => { select(options[0]); });
</script>

<ul class="text-right divide-y divide-sky-800 overflow-scroll snap-y">
    {#each options as option}
        <li class:hover:bg-slate-200={$parameter !== option}
            class:bg-slate-300={$parameter === option} class="p-2 snap-center">
            <button on:click={() => select(option)}>
                {option}
            </button>
        </li>
    {/each}
</ul>