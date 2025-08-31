#ifdef _WIN32
// The following should probably work to get inline working on Windows
// with MSVC, but it doesn't. So we just disable inlining for now.
//#  define inline __inline
//#  define INLINE static inline
# define DISABLE_INLINE 1


// Pari doesn't annotate those exports with __declspec(dllimport), so we
// need to use linker directives to avoid "unresolved external symbol" errors.
#pragma comment(linker, "/alternatename:win32ctrlc=__imp_win32ctrlc")
#pragma comment(linker, "/alternatename:PARI_SIGINT_block=__imp_PARI_SIGINT_block")
#pragma comment(linker, "/alternatename:PARI_SIGINT_pending=__imp_PARI_SIGINT_pending")
#pragma comment(linker, "/alternatename:pari_mainstack=__imp_pari_mainstack")
#pragma comment(linker, "/alternatename:avma=__imp_avma")
#pragma comment(linker, "/alternatename:gen_0=__imp_gen_0")
#pragma comment(linker, "/alternatename:cb_pari_err_handler=__imp_cb_pari_err_handler")
#pragma comment(linker, "/alternatename:cb_pari_err_recover=__imp_cb_pari_err_recover")
#pragma comment(linker, "/alternatename:GP_DATA=__imp_GP_DATA")
#pragma comment(linker, "/alternatename:pariOut=__imp_pariOut")
#pragma comment(linker, "/alternatename:LOG10_2=__imp_LOG10_2")
#pragma comment(linker, "/alternatename:new_galois_format=__imp_new_galois_format")
#pragma comment(linker, "/alternatename:factor_proven=__imp_factor_proven")
#pragma comment(linker, "/alternatename:precdl=__imp_precdl")
#pragma comment(linker, "/alternatename:gen_1=__imp_gen_1")
#pragma comment(linker, "/alternatename:gen_2=__imp_gen_2")
#pragma comment(linker, "/alternatename:gnil=__imp_gnil")
#pragma comment(linker, "/alternatename:ghalf=__imp_ghalf")
#pragma comment(linker, "/alternatename:err_e_STACK=__imp_err_e_STACK")
#pragma comment(linker, "/alternatename:cb_pari_err_handle=__imp_cb_pari_err_handle")

#endif // _WIN32
