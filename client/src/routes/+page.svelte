<script>
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcomeFallback from '$lib/images/svelte-welcome.png';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<h1 class="text-3xl font-bold underline">Hello world!</h1>

<style lang="postcss">
	:global(html) {
		background-color: theme(colors.gray.100);
	}
</style>
