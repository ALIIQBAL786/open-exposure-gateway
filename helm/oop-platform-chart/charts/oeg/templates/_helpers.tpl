{{/*
Expand the name of the chart.
*/}}
{{- define "oeg.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "oeg.fullname" -}}
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
{{- define "oeg.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "oeg.labels" -}}
helm.sh/chart: {{ include "oeg.chart" . }}
{{ include "oeg.selectorLabels" . }}
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
{{- define "oeg.selectorLabels" -}}
app.kubernetes.io/name: {{ include "oeg.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
MongoDB labels
*/}}
{{- define "oeg.mongodb.labels" -}}
helm.sh/chart: {{ include "oeg.chart" . }}
{{ include "oeg.mongodb.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
MongoDB selector labels
*/}}
{{- define "oeg.mongodb.selectorLabels" -}}
app.kubernetes.io/name: {{ .Values.mongodb.name }}
app.kubernetes.io/instance: {{ .Release.Name }}
io.kompose.service: {{ .Values.mongodb.name }}
{{- end }}

{{/*
OEG Controller labels
*/}}
{{- define "oeg.controller.labels" -}}
helm.sh/chart: {{ include "oeg.chart" . }}
{{ include "oeg.controller.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
OEG Controller selector labels
*/}}
{{- define "oeg.controller.selectorLabels" -}}
app.kubernetes.io/name: {{ .Values.oegcontroller.name }}
app.kubernetes.io/instance: {{ .Release.Name }}
io.kompose.service: {{ .Values.oegcontroller.name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "oeg.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "oeg.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Return the proper namespace
*/}}
{{- define "oeg.namespace" -}}
{{- default .Release.Namespace .Values.global.namespace }}
{{- end }}
