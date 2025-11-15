# Documentation: rust/dbn/src/python/enums.rs

## File Metadata

**Path:** `rust/dbn/src/python/enums.rs`
**Filename:** `enums.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../../rust/dbn/src/python/enums.rs`

### Source Content

```rs
use std::str::FromStr;

use pyo3::{prelude::*, type_object::PyTypeInfo, types::PyType, Bound};

use crate::{
    enums::{Compression, Encoding, SType, Schema, SecurityUpdateAction, UserDefinedInstrument},
    Action, InstrumentClass, MatchAlgorithm, RType, Side, StatType, StatusAction, StatusReason,
    TradingEvent, TriState, VersionUpgradePolicy,
};

use super::{to_py_err, EnumIterator, PyFieldDesc};

#[pymethods]
impl Side {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let Ok(i) = value.extract::<u8>() else {
            let t = Self::type_object(py);
            let c = value.extract::<char>().map_err(to_py_err)?;
            return Self::py_from_str(&t, c);
        };
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> String {
        format!("{}", *self as u8 as char)
    }

    fn __repr__(&self) -> String {
        format!("<Side.{}: '{}'>", self.name(), self.value())
    }

    #[getter]
    fn name(&self) -> String {
        self.as_ref().to_ascii_uppercase()
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> String {
        self.__str__()
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: char) -> PyResult<Self> {
        Self::try_from(value as u8).map_err(to_py_err)
    }
}

#[pymethods]
impl Action {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let Ok(i) = value.extract::<u8>() else {
            let t = Self::type_object(py);
            let c = value.extract::<char>().map_err(to_py_err)?;
            return Self::py_from_str(&t, c);
        };
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> String {
        format!("{}", *self as u8 as char)
    }

    fn __repr__(&self) -> String {
        format!("<Action.{}: '{}'>", self.name(), self.value())
    }

    #[getter]
    fn name(&self) -> String {
        self.as_ref().to_ascii_uppercase()
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> String {
        self.__str__()
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: char) -> PyResult<Self> {
        Self::try_from(value as u8).map_err(to_py_err)
    }
}

#[pymethods]
impl InstrumentClass {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let Ok(i) = value.extract::<u8>() else {
            let t = Self::type_object(py);
            let c = value.extract::<char>().map_err(to_py_err)?;
            return Self::py_from_str(&t, c);
        };
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> String {
        format!("{}", *self as u8 as char)
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> String {
        self.__str__()
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: char) -> PyResult<Self> {
        Self::try_from(value as u8).map_err(to_py_err)
    }
}

#[pymethods]
impl MatchAlgorithm {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let Ok(i) = value.extract::<u8>() else {
            let t = Self::type_object(py);
            let c = value.extract::<char>().map_err(to_py_err)?;
            return Self::py_from_str(&t, c);
        };
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> String {
        format!("{}", *self as u8 as char)
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> String {
        self.__str__()
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: char) -> PyResult<Self> {
        Self::try_from(value as u8).map_err(to_py_err)
    }
}

#[pymethods]
impl UserDefinedInstrument {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let Ok(i) = value.extract::<u8>() else {
            let t = Self::type_object(py);
            let c = value.extract::<char>().map_err(to_py_err)?;
            return Self::py_from_str(&t, c);
        };
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> String {
        format!("{}", *self as u8 as char)
    }

    fn __repr__(&self) -> String {
        format!(
            "<UserDefinedInstrument.{}: '{}'>",
            self.name(),
            self.value()
        )
    }

    #[getter]
    fn name(&self) -> String {
        self.as_ref().to_ascii_uppercase()
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> String {
        self.__str__()
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: char) -> PyResult<Self> {
        Self::try_from(value as u8).map_err(to_py_err)
    }
}

#[pymethods]
impl SType {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let t = Self::type_object(py);
        Self::py_from_str(&t, value)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> &'static str {
        self.as_str()
    }

    fn __repr__(&self) -> String {
        format!("<SType.{}: '{}'>", self.name(), self.value(),)
    }

    #[getter]
    fn name(&self) -> String {
        self.as_str().to_uppercase()
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> &'static str {
        self.as_str()
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: &Bound<PyAny>) -> PyResult<Self> {
        let value_str: String = value.str().and_then(|s| s.extract())?;
        let tokenized = value_str.replace('-', "_").to_lowercase();
        Ok(Self::from_str(&tokenized)?)
    }
}

#[pymethods]
impl RType {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let t = Self::type_object(py);
        Self::py_from_str(&t, value).or_else(|_| Self::py_from_int(&t, value))
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> &'static str {
        self.as_str()
    }

    fn __repr__(&self) -> String {
        format!("<RType.{}: '{}'>", self.name(), self.value(),)
    }

    #[getter]
    fn name(&self) -> String {
        self.as_str().to_uppercase()
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> u8 {
        *self as u8
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: &Bound<PyAny>) -> PyResult<Self> {
        let value_str: String = value.str().and_then(|s| s.extract())?;
        let tokenized = value_str.replace('-', "_").to_lowercase();
        Ok(Self::from_str(&tokenized)?)
    }

    #[classmethod]
    #[pyo3(name = "from_int")]
    fn py_from_int(_: &Bound<PyType>, value: &Bound<PyAny>) -> PyResult<Self> {
        let value: u8 = value.extract()?;
        Self::try_from(value).map_err(to_py_err)
    }

    #[classmethod]
    #[pyo3(name = "from_schema")]
    fn py_from_schema(pytype: &Bound<PyType>, value: &Bound<PyAny>) -> PyResult<Self> {
        let schema: Schema = value
            .extract()
            .or_else(|_| Schema::py_from_str(&Schema::type_object(pytype.py()), value))
            .map_err(to_py_err)?;
        Ok(Self::from(schema))
    }
}

#[pymethods]
impl Schema {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let t = Self::type_object(py);
        Self::py_from_str(&t, value)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> &'static str {
        self.as_str()
    }

    fn __repr__(&self) -> String {
        format!("<Schema.{}: '{}'>", self.name(), self.value(),)
    }

    #[getter]
    fn name(&self) -> String {
        self.as_str().to_uppercase()
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> &'static str {
        self.as_str()
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: &Bound<PyAny>) -> PyResult<Self> {
        let value_str: String = value.str().and_then(|s| s.extract())?;
        let tokenized = value_str.replace('_', "-").to_lowercase();
        Ok(Self::from_str(&tokenized)?)
    }
}

#[pymethods]
impl Encoding {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let t = Self::type_object(py);
        Self::py_from_str(&t, value)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> &'static str {
        self.as_str()
    }

    fn __repr__(&self) -> String {
        format!("<Encoding.{}: '{}'>", self.name(), self.value(),)
    }

    #[getter]
    fn name(&self) -> String {
        self.as_str().to_uppercase()
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> &'static str {
        self.as_str()
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: &Bound<PyAny>) -> PyResult<Self> {
        let value_str: String = value.str().and_then(|s| s.extract())?;
        let tokenized = value_str.to_lowercase();
        Ok(Self::from_str(&tokenized)?)
    }
}

#[pymethods]
impl Compression {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let t = Self::type_object(py);
        Self::py_from_str(&t, value)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> &'static str {
        self.as_str()
    }

    fn __repr__(&self) -> String {
        format!("<Compression.{}: '{}'>", self.name(), self.value(),)
    }

    #[getter]
    fn name(&self) -> String {
        self.as_str().to_uppercase()
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> &'static str {
        self.as_str()
    }

    // No metaclass support with pyo3, so `for c in Compression: ...` isn't possible
    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: &Bound<PyAny>) -> PyResult<Self> {
        let value_str: String = value.str().and_then(|s| s.extract())?;
        let tokenized = value_str.to_lowercase();
        Ok(Self::from_str(&tokenized)?)
    }
}

#[pymethods]
impl SecurityUpdateAction {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let Ok(i) = value.extract::<u8>() else {
            let t = Self::type_object(py);
            let c = value.extract::<char>().map_err(to_py_err)?;
            return Self::py_from_str(&t, c);
        };
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __repr__(&self) -> String {
        format!("<SecurityUpdateAction.{}: '{}'>", self.name(), self.value())
    }

    #[getter]
    fn name(&self) -> String {
        self.as_ref().to_ascii_uppercase()
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> u16 {
        *self as u16
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: char) -> PyResult<Self> {
        Self::try_from(value as u8).map_err(to_py_err)
    }
}

#[pymethods]
impl StatType {
    #[new]
    fn py_new(value: &Bound<PyAny>) -> PyResult<Self> {
        let i = value.extract::<u16>().map_err(to_py_err)?;
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __eq__(&self, other: &Bound<PyAny>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> u16 {
        *self as u16
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }
}

#[pymethods]
impl StatusAction {
    #[new]
    fn py_new(value: &Bound<PyAny>) -> PyResult<Self> {
        let i = value.extract::<u16>().map_err(to_py_err)?;
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __eq__(&self, other: &Bound<PyAny>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> u16 {
        *self as u16
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }
}

#[pymethods]
impl StatusReason {
    #[new]
    fn py_new(value: &Bound<PyAny>) -> PyResult<Self> {
        let i = value.extract::<u16>().map_err(to_py_err)?;
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __eq__(&self, other: &Bound<PyAny>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> u16 {
        *self as u16
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }
}

#[pymethods]
impl TradingEvent {
    #[new]
    fn py_new(value: &Bound<PyAny>) -> PyResult<Self> {
        let i = value.extract::<u16>().map_err(to_py_err)?;
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __eq__(&self, other: &Bound<PyAny>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> u16 {
        *self as u16
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }
}

#[pymethods]
impl TriState {
    #[new]
    fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
        let Ok(i) = value.extract::<u8>() else {
            let t = Self::type_object(py);
            let c = value.extract::<char>().map_err(to_py_err)?;
            return Self::py_from_str(&t, c);
        };
        Self::try_from(i).map_err(to_py_err)
    }

    fn __hash__(&self) -> isize {
        *self as isize
    }

    fn __str__(&self) -> String {
        format!("{}", *self as u8 as char)
    }

    fn opt_bool(&self) -> Option<bool> {
        Option::from(*self)
    }

    fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
        let Ok(other_enum) = other.extract::<Self>().or_else(|_| Self::py_new(py, other)) else {
            return false;
        };
        self.eq(&other_enum)
    }

    #[getter]
    fn value(&self) -> String {
        self.__str__()
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }

    #[classmethod]
    #[pyo3(name = "from_str")]
    fn py_from_str(_: &Bound<PyType>, value: char) -> PyResult<Self> {
        Self::try_from(value as u8).map_err(to_py_err)
    }
}

#[pymethods]
impl VersionUpgradePolicy {
    fn __hash__(&self) -> isize {
        *self as isize
    }

    #[classmethod]
    fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
        EnumIterator::new::<Self>(py)
    }
}

impl PyFieldDesc for SecurityUpdateAction {
    fn field_dtypes(field_name: &str) -> Vec<(String, String)> {
        vec![(field_name.to_owned(), "S1".to_owned())]
    }
}

impl PyFieldDesc for UserDefinedInstrument {
    fn field_dtypes(field_name: &str) -> Vec<(String, String)> {
        vec![(field_name.to_owned(), "S1".to_owned())]
    }
}

```

## High-Level Overview

This file is located at `rust/dbn/src/python/enums.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** __eq__, __hash__, __repr__, __str__, field_dtypes, name, opt_bool, py_from_int, py_from_schema, py_from_str, py_new, value, variants

**Dependencies:** This file imports from 4 modules


#### Detailed Walkthrough


##### Function: `py_new`

```rust
fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
```


##### Function: `__hash__`

```rust
fn __hash__(&self) -> isize {
```


##### Function: `__str__`

```rust
fn __str__(&self) -> String {
```


##### Function: `__repr__`

```rust
fn __repr__(&self) -> String {
```


##### Function: `name`

```rust
fn name(&self) -> String {
```


##### Function: `__eq__`

```rust
fn __eq__(&self, other: &Bound<PyAny>, py: Python<'_>) -> bool {
```


##### Function: `value`

```rust
fn value(&self) -> String {
```


##### Function: `variants`

```rust
fn variants(_: &Bound<PyType>, py: Python<'_>) -> PyResult<EnumIterator> {
```


##### Function: `py_from_str`

```rust
fn py_from_str(_: &Bound<PyType>, value: char) -> PyResult<Self> {
```


##### Function: `py_new`

```rust
fn py_new(py: Python<'_>, value: &Bound<PyAny>) -> PyResult<Self> {
```


*... and more functions (see source code)*


#### Architecture & Design

This file contributes to the overall DBN library architecture by providing essential functionality
for encoding, decoding, or representing market data in the Databento Binary Encoding format.

**Design Principles:**
- Type safety through Rust's strong type system
- Zero-cost abstractions for performance
- Clear error handling with Result types
- Memory efficiency for large-scale data processing

#### Performance Considerations

Rust's ownership model and zero-cost abstractions make this implementation highly performant:
- Stack allocation where possible
- Minimal heap allocations
- Compile-time optimizations
- No garbage collection overhead

#### Security & Safety

Rust's memory safety guarantees prevent:
- Buffer overflows
- Null pointer dereferences
- Data races in concurrent code
- Use-after-free bugs

All unsafe code blocks (if any) are carefully reviewed and documented.

