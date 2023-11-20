<script>
    import { createEventDispatcher } from "svelte";
    import MdAdd from "svelte-icons/md/MdAdd.svelte";

    const dispatch = createEventDispatcher();

    export let disabled;
</script>

<div class="h-1/4 w-full flex flex-col justify-center">
    <div class="mx-auto relative text-sky-800">
        <div class="p-0 h-10 text-emerald-500 absolute pointer-events-none -top-2 -left-4">
            <MdAdd/>
        </div>
        <button class="pt-1 w-10 disabled:text-sky-800/70" on:click={event => { dispatch("click") }} {disabled}>
            <slot name="button">
            </slot>
        </button>
    </div>
    <div class="text-center">
        <slot name="title">
        </slot>
    </div>
</div>