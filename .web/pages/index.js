/** @jsxImportSource @emotion/react */


import { ErrorBoundary } from "react-error-boundary"
import { Fragment, useCallback, useContext, useEffect, useState } from "react"
import { ColorModeContext, EventLoopContext, StateContexts } from "$/utils/context"
import { Event, getBackendURL, getRefValue, getRefValues, isTrue, refs } from "$/utils/state"
import { jsx, keyframes } from "@emotion/react"
import { WifiOffIcon as LucideWifiOffIcon } from "lucide-react"
import { toast, Toaster } from "sonner"
import env from "$/env.json"
import { Box as RadixThemesBox, Button as RadixThemesButton, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Select as RadixThemesSelect, Spinner as RadixThemesSpinner, Text as RadixThemesText, TextField as RadixThemesTextField } from "@radix-ui/themes"
import { Root as RadixFormRoot } from "@radix-ui/react-form"
import NextHead from "next/head"



export function Root_89d0f2806b303057b8a140b457222b85 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  
    const handleSubmit_44cf91d9470f038f0a6942ba9d889f67 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(Event("reflex___state____state.cuestio_extralab___cuestio_extralab____form_state.handle_submit", ({ ["form_data"] : form_data }), ({  })))], args, ({  }))))());

        if (true) {
            $form.reset()
        }
    })
    




  
  return (
    <RadixFormRoot className={"Root "} css={({ ["width"] : "100%" })} onSubmit={handleSubmit_44cf91d9470f038f0a6942ba9d889f67}>

<RadixThemesFlex align={"start"} className={"rx-Stack"} css={({ ["alignItems"] : "center" })} direction={"column"} gap={"4"}>

<RadixThemesTextField.Root color={"green"} css={({ ["textAlign"] : "center", ["textTransform"] : "capitalize", ["width"] : "280px", ["height"] : "40px", ["borderRadius"] : "25px", ["fontSize"] : "1.1rem", ["&:focus"] : ({ ["outline"] : "none", ["border"] : "2px green", ["boxShadow"] : "none" }) })} name={"cedula"} placeholder={"C\u00e9dula"}/>
<RadixThemesTextField.Root color={"green"} css={({ ["textAlign"] : "center", ["textTransform"] : "capitalize", ["width"] : "280px", ["height"] : "40px", ["borderRadius"] : "25px", ["fontSize"] : "1.1rem", ["&:focus"] : ({ ["outline"] : "none", ["border"] : "2px solid green", ["boxShadow"] : "none" }) })} name={"nombre_empleado"} placeholder={"Nombre de empleado"}/>
<RadixThemesSelect.Root css={({ ["textAlign"] : "center", ["width"] : "300px", ["height"] : "50px", ["borderRadius"] : "15px", ["fontSize"] : "1.1rem", ["padding"] : "0.5rem", ["appearance"] : "none", ["-webkit-appearance"] : "none", ["-moz-appearance"] : "none", ["boxShadow"] : "0 4px 10px rgba(0,128,0,0.3)", ["&:hover"] : ({ ["boxShadow"] : "0 4px 10px rgba(0,128,0,0.5)", ["cursor"] : "pointer" }) })} name={"tipo_empleado"} size={"3"}>

<RadixThemesSelect.Trigger color={"green"} placeholder={"Seleccione el tipo de empleado"} radius={"full"}/>
<RadixThemesSelect.Content color={"green"}>

<RadixThemesSelect.Group>

{""}
<RadixThemesSelect.Item value={"A"}>

{"A"}
</RadixThemesSelect.Item>
<RadixThemesSelect.Item value={"B"}>

{"B"}
</RadixThemesSelect.Item>
</RadixThemesSelect.Group>
</RadixThemesSelect.Content>
</RadixThemesSelect.Root>
<RadixThemesSelect.Root css={({ ["textAlign"] : "center", ["width"] : "300px", ["height"] : "50px", ["borderRadius"] : "15px", ["fontSize"] : "1.1rem", ["padding"] : "0.5rem", ["&:hover"] : ({ ["boxShadow"] : "0 4px 10px rgba(0,128,0,0.5)", ["cursor"] : "pointer" }) })} name={"area"} size={"3"}>

<RadixThemesSelect.Trigger color={"green"} placeholder={"Seleccione el \u00e1rea"} radius={"full"}/>
<RadixThemesSelect.Content color={"green"}>

<RadixThemesSelect.Group>

{""}
<RadixThemesSelect.Item value={"RRHH"}>

{"RRHH"}
</RadixThemesSelect.Item>
<RadixThemesSelect.Item value={"Operaciones"}>

{"Operaciones"}
</RadixThemesSelect.Item>
<RadixThemesSelect.Item value={"Mantenimiento"}>

{"Mantenimiento"}
</RadixThemesSelect.Item>
<RadixThemesSelect.Item value={"Financiera"}>

{"Financiera"}
</RadixThemesSelect.Item>
<RadixThemesSelect.Item value={"SGI"}>

{"SGI"}
</RadixThemesSelect.Item>
<RadixThemesSelect.Item value={"Gerencia"}>

{"Gerencia"}
</RadixThemesSelect.Item>
</RadixThemesSelect.Group>
</RadixThemesSelect.Content>
</RadixThemesSelect.Root>
<Button_4168d046a12212dd1195df69b3b388ac/>
</RadixThemesFlex>
</RadixFormRoot>
  )
}

export function Button_4168d046a12212dd1195df69b3b388ac () {
  
  const reflex___state____state__cuestio_extralab___cuestio_extralab____form_state = useContext(StateContexts.reflex___state____state__cuestio_extralab___cuestio_extralab____form_state)





  
  return (
    <RadixThemesButton css={({ ["width"] : "auto", ["minWidth"] : "140px", ["height"] : "40px", ["borderRadius"] : "1em", ["fontSize"] : "0.8rem", ["padding"] : "0.5rem 1rem", ["marginTop"] : "0.4rem", ["backgroundImage"] : "linear-gradient(144deg, #4CAF50, #388E3C 50%, #2E7D32)", ["boxShadow"] : "rgba(34, 139, 34, 0.8) 0 15px 30px -10px", ["color"] : "white", ["opacity"] : "1", ["transition"] : "transform 0.3s ease", ["&:hover"] : ({ ["transform"] : "scale(1.1)" }), ["isDisabled"] : reflex___state____state__cuestio_extralab___cuestio_extralab____form_state.show_loading })} type={"submit"}>

<Fragment_357ab848e84aeffdd5755e14b07a31df/>
</RadixThemesButton>
  )
}

export function Fragment_edf99f54ef7f0bff40365d02faafb0ab () {
  
  const reflex___state____state__cuestio_extralab___cuestio_extralab____form_state = useContext(StateContexts.reflex___state____state__cuestio_extralab___cuestio_extralab____form_state)





  
  return (
    <Fragment>

{isTrue(reflex___state____state__cuestio_extralab___cuestio_extralab____form_state.show_loading) ? (
  <Fragment>

<RadixThemesSpinner css={({ ["position"] : "fixed", ["top"] : "50%", ["left"] : "50%", ["transform"] : "translate(-50%, -50%)", ["zIndex"] : "1000", ["color"] : "green" })} size={"3"}/>
</Fragment>
) : (
  <Fragment>

<RadixThemesText as={"p"}>

{""}
</RadixThemesText>
</Fragment>
)}
</Fragment>
  )
}

export function Div_602c14884fa2de27f522fe8f94374b02 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);





  
  return (
    <div css={({ ["position"] : "fixed", ["width"] : "100vw", ["height"] : "0" })} title={("Connection Error: "+((connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : ''))}>

<Fragment_f2f0916d2fcc08b7cdf76cec697f0750/>
</div>
  )
}

export function Errorboundary_3d21f1dd1db1459e9bcdd98a3de8ada8 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_error_0f5dbf674521530422d73a7946faf6d4 = useCallback(((_error, _info) => (addEvents([(Event("reflex___state____state.reflex___state____frontend_event_exception_state.handle_frontend_exception", ({ ["stack"] : _error["stack"], ["component_stack"] : _info["componentStack"] }), ({  })))], [_error, _info], ({  })))), [addEvents, Event])



  
  return (
    <ErrorBoundary fallbackRender={((event_args) => (jsx("div", ({ ["css"] : ({ ["height"] : "100%", ["width"] : "100%", ["position"] : "absolute", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center" }) }), (jsx("div", ({ ["css"] : ({ ["display"] : "flex", ["flexDirection"] : "column", ["gap"] : "1rem" }) }), (jsx("div", ({ ["css"] : ({ ["display"] : "flex", ["flexDirection"] : "column", ["gap"] : "1rem", ["maxWidth"] : "50ch", ["border"] : "1px solid #888888", ["borderRadius"] : "0.25rem", ["padding"] : "1rem" }) }), (jsx("h2", ({ ["css"] : ({ ["fontSize"] : "1.25rem", ["fontWeight"] : "bold" }) }), (jsx(Fragment, ({  }), "An error occurred while rendering this page.")))), (jsx("p", ({ ["css"] : ({ ["opacity"] : "0.75" }) }), (jsx(Fragment, ({  }), "This is an error with the application itself.")))), (jsx("details", ({  }), (jsx("summary", ({ ["css"] : ({ ["padding"] : "0.5rem" }) }), (jsx(Fragment, ({  }), "Error message")))), (jsx("div", ({ ["css"] : ({ ["width"] : "100%", ["maxHeight"] : "50vh", ["overflow"] : "auto", ["background"] : "#000", ["color"] : "#fff", ["borderRadius"] : "0.25rem" }) }), (jsx("div", ({ ["css"] : ({ ["padding"] : "0.5rem", ["width"] : "fit-content" }) }), (jsx("pre", ({  }), (jsx(Fragment, ({  }), event_args.error.stack)))))))), (jsx("button", ({ ["css"] : ({ ["padding"] : "0.35rem 0.75rem", ["margin"] : "0.5rem", ["background"] : "#fff", ["color"] : "#000", ["border"] : "1px solid #000", ["borderRadius"] : "0.25rem", ["fontWeight"] : "bold" }), ["onClick"] : ((...args) => (addEvents([(Event("_call_function", ({ ["function"] : (() => (navigator["clipboard"]["writeText"](event_args.error.stack))), ["callback"] : null }), ({  })))], args, ({  })))) }), (jsx(Fragment, ({  }), "Copy")))))))), (jsx("hr", ({ ["css"] : ({ ["borderColor"] : "currentColor", ["opacity"] : "0.25" }) }))), (jsx("a", ({ ["href"] : "https://reflex.dev" }), (jsx("div", ({ ["css"] : ({ ["display"] : "flex", ["alignItems"] : "baseline", ["justifyContent"] : "center", ["fontFamily"] : "monospace", ["--default-font-family"] : "monospace", ["gap"] : "0.5rem" }) }), (jsx(Fragment, ({  }), "Built with ")), (jsx("svg", ({ ["css"] : ({ ["viewBox"] : "0 0 56 12", ["fill"] : "currentColor" }), ["height"] : "12", ["width"] : "56", ["xmlns"] : "http://www.w3.org/2000/svg" }), (jsx("path", ({ ["d"] : "M0 11.5999V0.399902H8.96V4.8799H6.72V2.6399H2.24V4.8799H6.72V7.1199H2.24V11.5999H0ZM6.72 11.5999V7.1199H8.96V11.5999H6.72Z" }))), (jsx("path", ({ ["d"] : "M11.2 11.5999V0.399902H17.92V2.6399H13.44V4.8799H17.92V7.1199H13.44V9.3599H17.92V11.5999H11.2Z" }))), (jsx("path", ({ ["d"] : "M20.16 11.5999V0.399902H26.88V2.6399H22.4V4.8799H26.88V7.1199H22.4V11.5999H20.16Z" }))), (jsx("path", ({ ["d"] : "M29.12 11.5999V0.399902H31.36V9.3599H35.84V11.5999H29.12Z" }))), (jsx("path", ({ ["d"] : "M38.08 11.5999V0.399902H44.8V2.6399H40.32V4.8799H44.8V7.1199H40.32V9.3599H44.8V11.5999H38.08Z" }))), (jsx("path", ({ ["d"] : "M47.04 4.8799V0.399902H49.28V4.8799H47.04ZM53.76 4.8799V0.399902H56V4.8799H53.76ZM49.28 7.1199V4.8799H53.76V7.1199H49.28ZM47.04 11.5999V7.1199H49.28V11.5999H47.04ZM53.76 11.5999V7.1199H56V11.5999H53.76Z" }))))))))))))))} onError={on_error_0f5dbf674521530422d73a7946faf6d4}>

<Fragment>

<Div_602c14884fa2de27f522fe8f94374b02/>
<Toaster_6e6ebf8d7ce589d59b7d382fb7576edf/>
</Fragment>
<RadixThemesFlex css={({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["background"] : "linear-gradient(to top, #0d4610, #6fbf73, #a4d17d)", ["height"] : "100vh", ["width"] : "100vw", ["flexDirection"] : "column", ["position"] : "relative", ["overflow"] : "hidden" })}>

<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "39px", ["height"] : "39px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "95%", ["left"] : "63%", ["animation"] : "moverAnim 9.379773543914338s ease-in-out infinite", ["animationDelay"] : "2.839220577677265s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "71px", ["height"] : "71px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "50%", ["left"] : "34%", ["animation"] : "moverAnim 8.242009034765399s ease-in-out infinite", ["animationDelay"] : "1.865794139880621s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "72px", ["height"] : "72px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "35%", ["left"] : "12%", ["animation"] : "moverAnim 11.924804274142986s ease-in-out infinite", ["animationDelay"] : "4.151458945464143s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "54px", ["height"] : "54px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "58%", ["left"] : "47%", ["animation"] : "moverAnim 7.149822219020015s ease-in-out infinite", ["animationDelay"] : "0.4785057770641199s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "57px", ["height"] : "57px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "71%", ["left"] : "32%", ["animation"] : "moverAnim 11.97892467289418s ease-in-out infinite", ["animationDelay"] : "3.5188567307007173s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "79px", ["height"] : "79px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "100%", ["left"] : "94%", ["animation"] : "moverAnim 10.78821695845894s ease-in-out infinite", ["animationDelay"] : "2.8649031211079405s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "74px", ["height"] : "74px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "3%", ["left"] : "65%", ["animation"] : "moverAnim 10.678988931084442s ease-in-out infinite", ["animationDelay"] : "0.8475943864041541s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "54px", ["height"] : "54px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "89%", ["left"] : "62%", ["animation"] : "moverAnim 11.08408238822522s ease-in-out infinite", ["animationDelay"] : "3.578889920058705s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "50px", ["height"] : "50px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "29%", ["left"] : "94%", ["animation"] : "moverAnim 11.05470350370669s ease-in-out infinite", ["animationDelay"] : "3.2860417560549515s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "65px", ["height"] : "65px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "100%", ["left"] : "69%", ["animation"] : "moverAnim 10.79781300354271s ease-in-out infinite", ["animationDelay"] : "0.26645458553911205s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "37px", ["height"] : "37px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "67%", ["left"] : "56%", ["animation"] : "moverAnim 10.40653230611194s ease-in-out infinite", ["animationDelay"] : "2.848631354353397s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "57px", ["height"] : "57px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "42%", ["left"] : "100%", ["animation"] : "moverAnim 9.84770717294775s ease-in-out infinite", ["animationDelay"] : "0.8793779410373215s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "77px", ["height"] : "77px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "64%", ["left"] : "89%", ["animation"] : "moverAnim 9.453141910514631s ease-in-out infinite", ["animationDelay"] : "2.5995352181423748s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "79px", ["height"] : "79px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "61%", ["left"] : "67%", ["animation"] : "moverAnim 9.800324325899744s ease-in-out infinite", ["animationDelay"] : "0.9677603043608857s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "34px", ["height"] : "34px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "96%", ["left"] : "38%", ["animation"] : "moverAnim 11.376676493392399s ease-in-out infinite", ["animationDelay"] : "3.2938597608095743s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "65px", ["height"] : "65px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "64%", ["left"] : "18%", ["animation"] : "moverAnim 9.134175569695376s ease-in-out infinite", ["animationDelay"] : "3.4191425646319864s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "38px", ["height"] : "38px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "4%", ["left"] : "90%", ["animation"] : "moverAnim 9.540395686375117s ease-in-out infinite", ["animationDelay"] : "3.1514870117041474s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "35px", ["height"] : "35px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "59%", ["left"] : "90%", ["animation"] : "moverAnim 11.33203872149804s ease-in-out infinite", ["animationDelay"] : "4.2198300834761495s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "79px", ["height"] : "79px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "45%", ["left"] : "91%", ["animation"] : "moverAnim 11.765920323985004s ease-in-out infinite", ["animationDelay"] : "2.590803670741979s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "33px", ["height"] : "33px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "91%", ["left"] : "57%", ["animation"] : "moverAnim 10.474358120791488s ease-in-out infinite", ["animationDelay"] : "0.09423868432775317s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "38px", ["height"] : "38px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "30%", ["left"] : "76%", ["animation"] : "moverAnim 11.831825049066849s ease-in-out infinite", ["animationDelay"] : "4.466611063136107s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "62px", ["height"] : "62px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "7%", ["left"] : "98%", ["animation"] : "moverAnim 7.581094172079903s ease-in-out infinite", ["animationDelay"] : "1.9448892297062248s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "62px", ["height"] : "62px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "72%", ["left"] : "6%", ["animation"] : "moverAnim 10.85563398136879s ease-in-out infinite", ["animationDelay"] : "3.5346174561774264s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "74px", ["height"] : "74px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "58%", ["left"] : "12%", ["animation"] : "moverAnim 7.099636271895634s ease-in-out infinite", ["animationDelay"] : "3.7432539877216424s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "68px", ["height"] : "68px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "54%", ["left"] : "33%", ["animation"] : "moverAnim 9.400450189033393s ease-in-out infinite", ["animationDelay"] : "2.811896555276986s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "42px", ["height"] : "42px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "53%", ["left"] : "49%", ["animation"] : "moverAnim 11.013705299199199s ease-in-out infinite", ["animationDelay"] : "0.4562767109093835s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "67px", ["height"] : "67px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "31%", ["left"] : "73%", ["animation"] : "moverAnim 8.264230077535174s ease-in-out infinite", ["animationDelay"] : "3.622898911498157s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "31px", ["height"] : "31px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "37%", ["left"] : "93%", ["animation"] : "moverAnim 6.033768889470184s ease-in-out infinite", ["animationDelay"] : "3.4010800784336133s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "55px", ["height"] : "55px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "84%", ["left"] : "20%", ["animation"] : "moverAnim 6.34697334567874s ease-in-out infinite", ["animationDelay"] : "0.04523809680433977s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["position"] : "absolute", ["width"] : "65px", ["height"] : "65px", ["backgroundColor"] : "rgba(255, 255, 255, 0.15)", ["borderRadius"] : "50%", ["top"] : "10%", ["left"] : "25%", ["animation"] : "moverAnim 11.896619126939372s ease-in-out infinite", ["animationDelay"] : "2.2417523172093508s", ["@keyframes moverAnim"] : ({ ["0%"] : ({ ["transform"] : "translate(0, 0)" }), ["50%"] : ({ ["transform"] : "translate(50px, -50px)" }), ["100%"] : ({ ["transform"] : "translate(0, 0)" }) }) })}/>
<RadixThemesBox css={({ ["background"] : "white", ["borderRadius"] : "30px", ["boxShadow"] : "0 5px 15px rgba(0,0,0,0.1)", ["padding"] : "1rem", ["width"] : "700px", ["height"] : "570px", ["overflow"] : "auto", ["display"] : "flex", ["flexDirection"] : "column", ["alignItems"] : "center", ["textAlign"] : "center", ["zIndex"] : "10" })}>

<RadixThemesFlex align={"start"} className={"rx-Stack"} direction={"column"} gap={"3"}>

<Fragment_edf99f54ef7f0bff40365d02faafb0ab/>
<img css={({ ["width"] : "120px", ["height"] : "120px", ["marginBottom"] : "0.1rem", ["alignSelf"] : "center", ["filter"] : "drop-shadow(0 2px 6px rgba(0, 0, 0, 0.3))", ["animation"] : "pulseShadow 3s ease-in-out infinite", ["transition"] : "transform 0.3s ease", ["&:hover"] : ({ ["transform"] : "scale(1.1)" }), ["@keyframes pulseShadow"] : ({ ["0%, 100%"] : ({ ["filter"] : "drop-shadow(0 2px 6px rgba(0, 0, 0, 0.3))" }), ["50%"] : ({ ["filter"] : "drop-shadow(0 4px 12px rgba(0, 0, 0, 0.5))" }) }) })} src={"/favicon.ico"}/>
<RadixThemesHeading css={({ ["marginTop"] : "0rem", ["marginBottom"] : "0.6rem", ["fontWeight"] : "extrabold", ["fontSize"] : "2.8rem", ["lineHeight"] : "1.2", ["padding"] : "0.5rem", ["textAlign"] : "center", ["backgroundImage"] : "linear-gradient(90deg, #27ae60, #1abc9c, #2ecc71)", ["backgroundSize"] : "150% auto", ["backgroundClip"] : "text", ["textFillColor"] : "transparent", ["animation"] : "gradientMove 6s ease infinite", ["textShadow"] : "0px 2px 4px rgba(0, 0, 0, 0.2)", ["@keyframes gradientMove"] : ({ ["0%"] : ({ ["backgroundPosition"] : "0% 0%" }), ["100%"] : ({ ["backgroundPosition"] : "100% 0%" }) }) })} size={"1"}>

{"Bater\u00eda de riesgo psicosocial"}
</RadixThemesHeading>
<Root_89d0f2806b303057b8a140b457222b85/>
<Fragment_3a7a0fc563b6262aa7369d1587f6c18a/>
</RadixThemesFlex>
</RadixThemesBox>
</RadixThemesFlex>
<NextHead>

<title>

{"Bater\u00eda de riesgo psicosocial"}
</title>
<meta content={"favicon.ico"} property={"og:image"}/>
</NextHead>
</ErrorBoundary>
  )
}

export function Fragment_f2f0916d2fcc08b7cdf76cec697f0750 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);





  
  return (
    <Fragment>

{isTrue((connectErrors.length > 0)) ? (
  <Fragment>

<LucideWifiOffIcon css={({ ["color"] : "crimson", ["zIndex"] : 9999, ["position"] : "fixed", ["bottom"] : "33px", ["right"] : "33px", ["animation"] : (pulse+" 1s infinite") })} size={32}/>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}

export function Fragment_3a7a0fc563b6262aa7369d1587f6c18a () {
  
  const reflex___state____state__cuestio_extralab___cuestio_extralab____form_state = useContext(StateContexts.reflex___state____state__cuestio_extralab___cuestio_extralab____form_state)





  
  return (
    <Fragment>

{isTrue(reflex___state____state__cuestio_extralab___cuestio_extralab____form_state.show_alert) ? (
  <Fragment>

<RadixThemesBox css={({ ["position"] : "fixed", ["top"] : "50%", ["left"] : "50%", ["transform"] : "translate(-50%, -50%)", ["background"] : "#f0f4f8", ["padding"] : "1rem", ["borderRadius"] : "12px", ["boxShadow"] : "0 5px 15px rgba(0,0,0,0.3)", ["zIndex"] : "1000", ["opacity"] : "1", ["transition"] : "opacity 1s ease-in-out" })}>

<RadixThemesText as={"p"} css={({ ["fontWeight"] : "bold", ["fontSize"] : "1.2rem" })}>

{"Resultados"}
</RadixThemesText>
<RadixThemesText as={"p"} size={"4"}>

{reflex___state____state__cuestio_extralab___cuestio_extralab____form_state.resultado_backend.at(0)}
</RadixThemesText>
<RadixThemesText as={"p"} size={"4"}>

{reflex___state____state__cuestio_extralab___cuestio_extralab____form_state.resultado_backend.at(1)}
</RadixThemesText>
</RadixThemesBox>
</Fragment>
) : (
  <Fragment>

<RadixThemesText as={"p"}>

{""}
</RadixThemesText>
</Fragment>
)}
</Fragment>
  )
}

export function Toaster_6e6ebf8d7ce589d59b7d382fb7576edf () {
  
  const { resolvedColorMode } = useContext(ColorModeContext)

  refs['__toast'] = toast
  const [addEvents, connectErrors] = useContext(EventLoopContext);
  const toast_props = ({ ["description"] : ("Check if server is reachable at "+getBackendURL(env.EVENT).href), ["closeButton"] : true, ["duration"] : 120000, ["id"] : "websocket-error" });
  const [userDismissed, setUserDismissed] = useState(false);
  (useEffect(
() => {
    if ((connectErrors.length >= 2)) {
        if (!userDismissed) {
            toast.error(
                `Cannot connect to server: ${((connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : '')}.`,
                {...toast_props, onDismiss: () => setUserDismissed(true)},
            )
        }
    } else {
        toast.dismiss("websocket-error");
        setUserDismissed(false);  // after reconnection reset dismissed state
    }
}
, [connectErrors]))




  
  return (
    <Toaster closeButton={false} expand={true} position={"bottom-right"} richColors={true} theme={resolvedColorMode}/>
  )
}

export function Fragment_357ab848e84aeffdd5755e14b07a31df () {
  
  const reflex___state____state__cuestio_extralab___cuestio_extralab____form_state = useContext(StateContexts.reflex___state____state__cuestio_extralab___cuestio_extralab____form_state)





  
  return (
    <Fragment>

{isTrue(reflex___state____state__cuestio_extralab___cuestio_extralab____form_state.show_loading) ? (
  <Fragment>

<RadixThemesFlex align={"start"} className={"rx-Stack"} direction={"row"} gap={"3"}>

<RadixThemesSpinner css={({ ["color"] : "white" })} size={"1"}/>
<RadixThemesText as={"p"} css={({ ["ml"] : "2" })}>

{"Procesando..."}
</RadixThemesText>
</RadixThemesFlex>
</Fragment>
) : (
  <Fragment>

<RadixThemesText as={"p"}>

{"Procesar empleado"}
</RadixThemesText>
</Fragment>
)}
</Fragment>
  )
}

const pulse = keyframes`
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
`


export default function Component() {
    




  return (
    <Errorboundary_3d21f1dd1db1459e9bcdd98a3de8ada8/>
  )
}
