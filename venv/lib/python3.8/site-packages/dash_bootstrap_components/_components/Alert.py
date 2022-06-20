# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Alert(Component):
    """An Alert component.
Alert allows you to create contextual feedback messages on user actions.

Control the visibility using callbacks with the `is_open` prop, or set it to
auto-dismiss with the `duration` prop.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  Often used with CSS to
    style elements with common properties.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- color (string; default 'success'):
    Alert color, options: primary, secondary, success, info, warning,
    danger, link or any valid CSS color of your choice (e.g. a hex
    code, a decimal code or a CSS color name) Default: secondary.

- dismissable (boolean; optional):
    If True, add a close button that allows Alert to be dismissed.

- duration (number; optional):
    Duration in milliseconds after which the Alert dismisses itself.

- fade (boolean; optional):
    If True, a fade animation will be applied when `is_open` is
    toggled. If False the Alert will simply appear and disappear.

- is_open (boolean; default True):
    Whether alert is open. Default: True.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, color=Component.UNDEFINED, is_open=Component.UNDEFINED, fade=Component.UNDEFINED, dismissable=Component.UNDEFINED, duration=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'class_name', 'color', 'dismissable', 'duration', 'fade', 'is_open', 'key', 'loading_state', 'style']
        self._type = 'Alert'
        self._namespace = 'dash_bootstrap_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'class_name', 'color', 'dismissable', 'duration', 'fade', 'is_open', 'key', 'loading_state', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Alert, self).__init__(children=children, **args)
