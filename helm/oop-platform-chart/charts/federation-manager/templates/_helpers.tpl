{{/*
Expand the name of the chart.
*/}}
{{- define "federation-manager.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "federation-manager.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "federation-manager.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "federation-manager.labels" -}}
helm.sh/chart: {{ include "federation-manager.chart" . }}
{{ include "federation-manager.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "federation-manager.selectorLabels" -}}
app.kubernetes.io/name: {{ include "federation-manager.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Keycloak labels
*/}}
{{- define "federation-manager.keycloak.labels" -}}
{{ include "federation-manager.labels" . }}
app: keycloak
{{- end }}

{{/*
Keycloak selector labels
*/}}
{{- define "federation-manager.keycloak.selectorLabels" -}}
app: keycloak
{{- end }}

{{/*
Federation Manager labels
*/}}
{{- define "federation-manager.fm.labels" -}}
{{ include "federation-manager.labels" . }}
app: federation-manager
{{- end }}

{{/*
Federation Manager selector labels
*/}}
{{- define "federation-manager.fm.selectorLabels" -}}
app: federation-manager
{{- end }}

{{/*
Namespace
*/}}
{{- define "federation-manager.namespace" -}}
{{- default .Values.global.namespace .Release.Namespace }}
{{- end }}
