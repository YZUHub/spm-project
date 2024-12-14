<script>
	import Header from './Header.svelte';
	import '../app.css';
	import { page } from '$app/stores';
	import { isAuthenticated, user } from '../stores/auth.js';

	let authenticated;
	let userDetails;

	// Use Svelte's `$` syntax for reactivity
	$: authenticated = $isAuthenticated;
	$: userDetails = $user;

	const isLoginPage = $page.url.pathname === '/login';
</script>

<div class="app">
	{#if authenticated || isLoginPage}
		{#if !isLoginPage}
			<Header />
		{/if}
		<main>
			<slot />
		</main>
		{#if !isLoginPage}
			<footer>
				<p>
					Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to learn about SvelteKit.
				</p>
			</footer>
		{/if}
	{/if}

	{#if !authenticated && !isLoginPage}
		<script>
			window.location.href = '/login';
		</script>
	{/if}
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 75%;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	footer a {
		font-weight: bold;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
